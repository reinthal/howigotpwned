import tempfile
import zipfile
from io import BytesIO
from typing import List

from dagster import AssetExecutionContext, asset
from dagster_aws.s3 import S3Resource

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.utils.uploader import Uploader

SOURCE_BUCKET='leaks'
TARGET_BUCKET='raw'
FOLDER_PATH='Cit0/Cit0day.in_special_for_xss.is/Cit0day Prem [_special_for_xss.is]'

@asset
def cit0day_prem_special_for_xssis_file_list(
    context: AssetExecutionContext, 
    s3: S3Resource) -> List[str]:
    """All password dumps and puts in minio"""
    response = s3.get_client().list_objects(Bucket=SOURCE_BUCKET, Marker=FOLDER_PATH)
    archives = [obj["Key"] for obj in response["Contents"]]
    context.instance.add_dynamic_partitions(password_archive_partitions_def.name, \
        partition_keys=archives)
    return archives

@asset(
    partitions_def=password_archive_partitions_def,
    deps=[cit0day_prem_special_for_xssis_file_list]
)
def cit0day_uncompressed(context: AssetExecutionContext, s3: S3Resource):
    archive = context.partition_key
    
    with tempfile.NamedTemporaryFile() as tf:
        s3.get_client().download_file(SOURCE_BUCKET, archive, tf.name) 
        ul = Uploader(s3, TARGET_BUCKET)
        ul.copy_archive_to_s3(tf.name, parent_key=archive)
    
    context.log.info(f"Uploaded {archive} to `{TARGET_BUCKET}`")
    
