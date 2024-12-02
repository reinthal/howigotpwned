import re
import uuid
from io import BytesIO
from typing import List

import polars as pl
from dagster import AssetExecutionContext, asset
from dagster_aws.s3 import S3Resource
from elasticsearch import Elasticsearch, helpers
from tqdm import tqdm

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.resources import ElasticResource, NessieCatalogResource
from dagster_project.schemas import (
    cit0day_partition_spec,
    cit0day_polars_schema,
    cit0day_schema,
    cit0day_sort_order,
    passwords_mappings,
)
from dagster_project.utils.iceberg_retry import append_to_table_with_retry
from dagster_project.utils.passwords import create_passwords_polars_frame_from_file
from dagster_project.utils.s3_utils import (
    get_objects,
)

RAW_BUCKET = "raw"
FOLDER_PATH = "extracted"
CATEGORY_REGEX = r".*\((?P<category>.*?)\)"
# How much data to load before flush to parquet
PARQUET_ESTIMATE_SIZE = 500.0


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
            df = create_passwords_polars_frame_from_file(
                file_obj, cit0day_polars_schema
            )

            match = re.search(CATEGORY_REGEX, file_name)
            if match:
                category = match.group("category")
            else:
                category = "no category"

            df = df.with_columns(
                (pl.lit(RAW_BUCKET)).alias("bucket"),
                (pl.lit(file_name)).alias("prefix"),
                (pl.lit(category).alias("category")),
                (pl.date(year=2020, month=11, day=4).alias("date")),
            )
            dfs = pl.concat([dfs, df])
            # Flush when file gets large enough or last object in list
            if dfs.estimated_size("mb") > PARQUET_ESTIMATE_SIZE or obj is obj[-1]:
                uid = uuid.uuid4()
                buffer = BytesIO()
                dfs.write_parquet(buffer)
                buffer.seek(0)
                Key = f"parquets/{uid}.parquet"
                nas_minio.get_client().upload_fileobj(
                    buffer, Bucket=RAW_BUCKET, Key=Key
                )
                dfs = pl.DataFrame(schema=cit0day_polars_schema)  # Reset the DataFrame
                context.log.info(
                    f"Progress: {pbar.n}/{pbar.total} \
                ({pbar.n / pbar.total * 100:.2f}%)"
                )  # Print status
            else:
                dfs = pl.concat([dfs, df])
            pbar.update(1)


@asset(group_name="raw", deps=[cit0day_as_parquet])
def cit0day_parquets(
    context: AssetExecutionContext,
    nas_minio: S3Resource,
) -> List[str]:
    """Parquet asset for all password dump archives"""
    archives = get_objects(source_bucket=RAW_BUCKET, prefix="parquets", s3=nas_minio)

    context.instance.add_dynamic_partitions(
        password_archive_partitions_def.name, partition_keys=archives
    )
    return archives


@asset(
    partitions_def=password_archive_partitions_def,
    group_name="elastic",
    description="Elastic data of Cit0day passwords.",
    deps=[cit0day_parquets],
)
def cit0day_elastic_passwords(
    context: AssetExecutionContext, nas_minio: S3Resource, elastic: ElasticResource
) -> None:
    upstream_archive = context.partition_key

    # Instantiate elastic

    client: Elasticsearch = Elasticsearch(hosts=[elastic.url], api_key=elastic.api_key)
    # download the file
    file_obj = BytesIO()
    nas_minio.get_client().download_fileobj(RAW_BUCKET, upstream_archive, file_obj)
    file_obj.seek(0)
    df = pl.read_parquet(file_obj)

    if not client.indices.exists(index=elastic.password_index):
        client.indices.create(index=elastic.password_index, body=passwords_mappings)
        context.log.info(f"Index '{elastic.password_index}' created successfully!")

    context.log.info(df.head())
    context.log.info(f"Filename: {upstream_archive}, df.shape: {df.shape}")
    docs = df.to_dicts()
    actions = [{"_index": elastic.password_index, "_source": doc} for doc in docs]
    resp = helpers.bulk(client, actions)
    context.log.info(resp)


@asset(
    partitions_def=password_archive_partitions_def,
    group_name="staging",
    description="Staged Cit0day passwords parsed.",
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
    # download the file
    file_obj = BytesIO()
    nas_minio.get_client().download_fileobj(RAW_BUCKET, upstream_archive, file_obj)
    file_obj.seek(0)
    df = pl.read_parquet(file_obj)
    pa_df = df.to_arrow()
    context.log.info(df.head())
    context.log.info(f"Filename: {upstream_archive}, df.shape: {df.shape}")
    context.log.info(f"Pyarrow frame, {pa_df.shape}")
    append_to_table_with_retry(pa_df, "staging.cit0day_password_files", catalog)
