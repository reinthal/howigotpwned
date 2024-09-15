from io import BytesIO
import tempfile
from typing import List

from dagster import AssetExecutionContext, asset, EnvVar
from dagster_aws.s3 import S3Resource

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.utils import copy_archive_to_s3, get_objects
from pyiceberg.catalog import load_catalog
import polars as pl
LEAKS_BUCKET='leaks'
RAW_BUCKET='raw'
FOLDER_PATH='Cit0/Cit0day.in_special_for_xss.is/Cit0day Prem [_special_for_xss.is]'

@asset
def cit0day_prem_special_for_xssis_archives(
    context: AssetExecutionContext, 
    s3: S3Resource) -> List[str]:
    """Asset for all password dump archives"""
    archives = get_objects(source_bucket=LEAKS_BUCKET, prefix=FOLDER_PATH, s3=s3)

    context.instance.add_dynamic_partitions(password_archive_partitions_def.name, \
            partition_keys=archives)
    return archives

@asset(
    partitions_def=password_archive_partitions_def,
    deps=[cit0day_prem_special_for_xssis_archives]
)
def cit0day_uncompressed(context: AssetExecutionContext, s3: S3Resource):
    archive = context.partition_key
    
    with tempfile.NamedTemporaryFile() as tf:
        s3.get_client().download_file(LEAKS_BUCKET, archive, tf.name) 
        copy_archive_to_s3(s3, RAW_BUCKET, tf.name, parent_key=archive)
    
    context.log.info(f"Uploaded {archive} to `{RAW_BUCKET}`")
    return s3.get_client().list_objects


# get all objects in raw
@asset(
    partitions_def=password_archive_partitions_def,
    group_name="staging",
    deps=[cit0day_uncompressed]
)
def cit0day_password_files(
    context: AssetExecutionContext, s3: S3Resource
) -> pl.DataFrame:
    import pyarrow as pa
    pa_strings = pa.string()
    password_files_pyarrow_schema = pa.schema([
        ('email', pa_strings),
        ('data', pa_strings),
        ('bucket', pa_strings),
        ('prefix', pa_strings),
    ]
    )
    password_files_polars_schema = pl.Schema({
        "email": pl.String(),
        "data": pl.String(),
        })
    catalog = load_catalog("default",
           **{
             "warehouse": EnvVar("DESTINATION__CATALOG__WAREHOUSE"),
              "uri": EnvVar("DESTINATION__CATALOG__URI"),
              "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
              "s3.endpoint": EnvVar("DESTINATION__CATALOG__S3_ENDPOINT"),
              "s3.access-key-id": EnvVar("DESTINATION__CATALOG__ACCESS_KEY_ID"),
              "s3.secret-access-key": EnvVar("DESTINATION__CATALOG__SECRET_ACCESS_KEY"),
              "type": EnvVar("DESTINATION__CATALOG__TYPE")
    })
    catalog.create_namespace_if_not_exists("staging")
    table = catalog.create_table_if_not_exists("staging.cit0day_password_files", schema=password_files_pyarrow_schema)

    upstream_archive = context.partition_key
    objs = get_objects(source_bucket=RAW_BUCKET, prefix=upstream_archive, s3=s3)

    for obj in objs:
        context.log.info(obj)
        # - file name
        file_name = obj
        # download the file
        file_obj = BytesIO()
        s3.get_client().download_file(RAW_BUCKET, file_name, file_obj)
        df = pl.read_csv(file_obj, has_header=False, separator=":", schema=password_files_polars_schema)
        df.with_columns(
            (pl.lit(RAW_BUCKET)).alias("bucket"),
            (pl.lit(file_name)).alias("prefix")
        )
        py_df = df.to_arrow()
        table.append(py_df)

    return df
    