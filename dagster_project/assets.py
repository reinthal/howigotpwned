from io import BytesIO
from typing import List

import polars as pl
from dagster import AssetExecutionContext, EnvVar, asset
from dagster_aws.s3 import S3Resource
from pyiceberg.catalog import load_catalog

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.utils.iceberg_retry import append_to_table_with_retry
from dagster_project.utils.s3_utils import get_objects

RAW_BUCKET = "raw"
FOLDER_PATH = "extracted"


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
def cit0day_password_files(context: AssetExecutionContext, s3: S3Resource) -> None:
    import pyarrow as pa

    pa_strings = pa.string()
    password_files_pyarrow_schema = pa.schema(
        [
            ("email", pa_strings),
            ("data", pa_strings),
            ("bucket", pa_strings),
            ("prefix", pa_strings),
        ]
    )
    password_files_polars_schema = pl.Schema(
        {
            "email": pl.String(),
            "data": pl.String(),
            "bucket": pl.String(),
            "prefix": pl.String(),
        }
    )
    catalog = load_catalog(
        "default",
        **{
            "warehouse": "s3://iceberg/warehouse",
            "uri": "https://nessie.local.reinthal.cc/iceberg/",
            "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
            "s3.endpoint": EnvVar(
                "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_S3_ENDPOINT"
            ).get_value(),
            "s3.access-key-id": EnvVar(
                "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"
            ).get_value(),
            "s3.secret-access-key": EnvVar(
                "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"
            ).get_value(),
            "type": "rest",
        },
    )
    catalog.create_namespace_if_not_exists("staging")
    catalog.create_table_if_not_exists(
        "staging.cit0day_password_files", schema=password_files_pyarrow_schema
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
        df = pl.read_csv(
            file_obj,
            has_header=False,
            separator=":",
            schema=password_files_polars_schema,
        )

        pa_df = df.with_columns(
            (pl.lit(RAW_BUCKET)).alias("bucket"), (pl.lit(file_name)).alias("prefix")
        ).to_arrow()
        append_to_table_with_retry(pa_df, "staging.cit0day_password_files", catalog)
