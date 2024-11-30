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
            if dfs.estimated_size("mb") > 300.0 or obj is obj[-1]:
                uid = uuid.uuid4()  # Define how to generate a unique identifier
                buffer = BytesIO()
                dfs.write_parquet(buffer)
                buffer.seek(0)
                Key =  f"parquets/{uid}.parquet"
                nas_minio.get_client().upload_fileobj(buffer,Bucket=RAW_BUCKET, Key=Key)
                print(f"Data written to {Key} and DataFrame reset. \
                    Esitmated file sizes: {dfs.estimated_size("mb") }")
                dfs = pl.DataFrame(schema=cit0day_polars_schema)  # Reset the DataFrame
                context.log.info(f'Progress: {pbar.n}/{pbar.total} \
                ({pbar.n / pbar.total * 100:.2f}%)')
            else:
                dfs = pl.concat([dfs, df])
            pbar.update(1)

@asset(group_name="raw")
def cit0day_prem_special_for_xssis_archives(
    context: AssetExecutionContext, nas_minio: S3Resource
) -> List[str]:
    """Asset for all password dump archives"""
    archives = get_directories(source_bucket=RAW_BUCKET, prefix=FOLDER_PATH,\
         s3=nas_minio)

    context.instance.add_dynamic_partitions(
        password_archive_partitions_def.name, partition_keys=archives
    )
    return archives


# get all objects in raw
@asset(
    partitions_def=password_archive_partitions_def,
    group_name="staging",
    description="Staged Cit0day passwords parsed as csv separated by `:`",
    deps=[cit0day_prem_special_for_xssis_archives],
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
    )

    upstream_archive = context.partition_key
    objs = get_objects(source_bucket=RAW_BUCKET, prefix=upstream_archive, s3=nas_minio)
    dfs = pl.DataFrame(schema=cit0day_polars_schema)
    for obj in objs:
        context.log.info(obj)
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
        context.log.info(f"Filename: {file_name}, df.shape: {df.shape}")
        dfs = pl.concat([dfs, df])

    append_to_table_with_retry(
        dfs.to_arrow(), "staging.cit0day_password_files", catalog
    )
