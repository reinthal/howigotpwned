import re
from io import BytesIO
from typing import List

import polars as pl
from dagster import AssetExecutionContext, asset
from dagster_aws.s3 import S3Resource

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.resources import NessieCatalogResource
from dagster_project.schemas import (
    cit0day_partition_spec,
    cit0day_polars_schema,
    cit0day_schema,
)
from dagster_project.utils.iceberg_retry import append_to_table_with_retry
from dagster_project.utils.passwords import create_passwords_polars_frame_from_file
from dagster_project.utils.s3_utils import get_objects

RAW_BUCKET = "raw"
FOLDER_PATH = "extracted"
CATEGORY_REGEX = r".*\((?P<category>.*?)\)"


@asset(group_name="raw")
def cit0day_prem_special_for_xssis_archives(
    context: AssetExecutionContext, s3: S3Resource
) -> List[str]:
    """Asset for all password dump archives"""
    archives = get_objects(source_bucket=RAW_BUCKET, prefix=FOLDER_PATH, s3=s3)

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
    s3: S3Resource,
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
    objs = get_objects(source_bucket=RAW_BUCKET, prefix=upstream_archive, s3=s3)

    for obj in objs:
        context.log.info(obj)
        # - file name
        file_name = obj
        # download the file
        file_obj = BytesIO()
        s3.get_client().download_fileobj(RAW_BUCKET, file_name, file_obj)
        df = create_passwords_polars_frame_from_file(file_obj, cit0day_polars_schema)

        match = re.search(CATEGORY_REGEX, file_name)
        if match:
            category = match.group("category")
        else:
            category = "no category"

        pa_df = df.with_columns(
            (pl.lit(RAW_BUCKET)).alias("bucket"),
            (pl.lit(file_name)).alias("prefix"),
            (pl.lit(category).alias("category")),
        ).to_arrow()
        context.log.info(f"Filename: {file_name}, df.shape: {df.shape}")
        append_to_table_with_retry(pa_df, "staging.cit0day_password_files", catalog)
