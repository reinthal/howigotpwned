import os
import re
import tempfile
import uuid
from io import BytesIO
from pathlib import Path
from typing import List

import polars as pl
from dagster import AssetExecutionContext, asset
from dagster_aws.s3 import S3Resource
from tqdm import tqdm

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.resources import NessieCatalogResource
from dagster_project.schemas import (
    cit0day_partition_spec,
    cit0day_sort_order,
    cit0day_polars_schema,
    cit0day_schema,
)
from dagster_project.utils.iceberg_retry import append_to_table_with_retry
from dagster_project.utils.passwords import create_passwords_polars_frame_from_file
from dagster_project.utils.s3_utils import (
    get_directories,
    get_objects,
)

RAW_BUCKET = "raw"
FOLDER_PATH = "extracted"
CATEGORY_REGEX = r".*\((?P<category>.*?)\)"
# How much data to load before flush to parquet
PARQUET_ESTIMATE_SIZE=500.0

@asset(group_name="raw")
def cit0day_as_parquet(context: AssetExecutionContext, nas_minio: S3Resource):
    objs = get_objects(source_bucket=RAW_BUCKET, prefix=FOLDER_PATH, s3=nas_minio)
    dfs = pl.DataFrame(schema=cit0day_polars_schema)
    with tqdm(total=len(objs)) as pbar:
        for obj in objs:
            # - file name
            file_name = obj
            # download the file
            file_obj = BytesIO()
            nas_minio.get_client().download_fileobj(RAW_BUCKET, file_name, file_obj)
            df = create_passwords_polars_frame_from_file(file_obj, cit0day_polars_schema)

            match = re.search(CATEGORY_REGEX, file_name)
            if match:
                category = match.group("category")
            else:
                category = "no category"

            df = df.with_columns(
                (pl.lit(RAW_BUCKET)).alias("bucket"),
                (pl.lit(file_name)).alias("prefix"),
                (pl.lit(category).alias("category")),
            )
            dfs = pl.concat([dfs, df])
            # Flush when file gets large enough or last object in list
            if dfs.estimated_size("mb") > PARQUET_ESTIMATE_SIZE or obj is obj[-1]:
                uid = uuid.uuid4()
                buffer = BytesIO()
                dfs.write_parquet(buffer)
                buffer.seek(0)
                Key =  f"parquets/{uid}.parquet"
                nas_minio.get_client().upload_fileobj(buffer,Bucket=RAW_BUCKET, Key=Key)
                print(f"Data written to {Key} and DataFrame reset. \
                    Esitmated file sizes: {dfs.estimated_size("mb") }")
                dfs = pl.DataFrame(schema=cit0day_polars_schema)  # Reset the DataFrame
                context.log.info(f'Progress: {pbar.n}/{pbar.total} \
                ({pbar.n / pbar.total * 100:.2f}%)') # Print status
            else:
                dfs = pl.concat([dfs, df])
            pbar.update(1)

@asset(group_name="raw", deps=[cit0day_as_parquet])
def cit0day_parquets(
    context: AssetExecutionContext, nas_minio: S3Resource, 
) -> List[str]:
    """Parquet asset for all password dump archives"""
    archives = get_objects(source_bucket=RAW_BUCKET, prefix="parquets",\
         s3=nas_minio)

    context.instance.add_dynamic_partitions(
        password_archive_partitions_def.name, partition_keys=archives
    )
    return archives


@asset(
    partitions_def=password_archive_partitions_def,
    group_name="staging",
    description="Staged Cit0day passwords parsed as csv separated by `:`",
    deps=[cit0day_parquets],
)
def cit0day_password_files(
    context: AssetExecutionContext,
    nas_minio: S3Resource,
    nessie_default: NessieCatalogResource,
) -> None:
    catalog = nessie_default.get_catalog()
    catalog.create_namespace_if_not_exists("staging")
    catalog.create_table_if_not_exists(
        "staging.cit0day_password_files",
        schema=cit0day_schema,
        partition_spec=cit0day_partition_spec,
        sort_order=cit0day_sort_order,
    )
    upstream_archive = context.partition_key
    dfs = pl.DataFrame(schema=cit0day_polars_schema)
    # download the file
    file_obj = BytesIO()
    nas_minio.get_client().download_fileobj(RAW_BUCKET, upstream_archive, file_obj)
    file_obj.seek(0)
    df = pl.read_parquet(file_obj)
    context.log.info(df.head())
    context.log.info(f"Filename: {upstream_archive}, df.shape: {df.shape}")
    pa_df = dfs.to_arrow()
    context.log.info(f"Pyarrow frame, {pa_df.shape}")
    append_to_table_with_retry(
        pa_df, "staging.cit0day_password_files", catalog
    )
