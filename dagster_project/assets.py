import tempfile
from typing import List

from dagster import AssetExecutionContext, asset
from dagster_aws.s3 import S3Resource

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.utils import copy_archive_to_s3, get_objects
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
    deps=[cit0day_uncompressed]
)
def cit0day_password_files(
    context: AssetExecutionContext, s3: S3Resource
) -> pl.DataFrame:
    upstream_archive = context.partition_key
    objs = get_objects(source_bucket=RAW_BUCKET, prefix=upstream_archive, s3=s3)
    for obj in objs:
        context.log.info(obj)
    return pl.DataFrame()
    