import tempfile
from typing import List

from dagster import AssetExecutionContext, asset
from dagster_aws.s3 import S3Resource

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.utils.uploader import copy_archive_to_s3

SOURCE_BUCKET='leaks'
TARGET_BUCKET='raw'
FOLDER_PATH='Cit0/Cit0day.in_special_for_xss.is/Cit0day Prem [_special_for_xss.is]'

@asset
def cit0day_prem_special_for_xssis_archives(
    context: AssetExecutionContext, 
    s3: S3Resource) -> List[str]:
    """Asset for all password dump archives"""
    paginator = s3.get_client().get_paginator("list_objects")
    response_iterator = paginator.paginate(Bucket=SOURCE_BUCKET, Prefix=FOLDER_PATH)

    # do the paginator loop
    for page in iter(response_iterator):
        # loop over each page
        archives = [obj["Key"] for obj in page["Contents"]]
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
        s3.get_client().download_file(SOURCE_BUCKET, archive, tf.name) 
        copy_archive_to_s3(s3, TARGET_BUCKET, tf.name, parent_key=archive)
    
    context.log.info(f"Uploaded {archive} to `{TARGET_BUCKET}`")
    
