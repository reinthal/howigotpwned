
import zipfile
from io import BytesIO
from typing import List

from dagster import AssetExecutionContext, asset
from dagster_aws.s3 import S3Resource

from dagster_project.partitions import password_archive_partitions_def
from dagster_project.utils import unpack

SOURCE_BUCKET='leaks'
TARGET_BUCKET='raw'
FOLDER_PATH='Cit0/Cit0day.in_special_for_xss.is/Cit0day Prem [_special_for_xss.is]'

@asset
def cit0day_prem_special_for_xssis_file_list(
    context: AssetExecutionContext, 
    s3: S3Resource) -> List[str]:
    """All password dumps and puts in minio"""
    response = s3.get_client().list_objects(Bucket=SOURCE_BUCKET, Marker=FOLDER_PATH)
    archives = [obj["Key"] for obj in response["Contents"]][:100]
    context.instance.add_dynamic_partitions(password_archive_partitions_def.name, \
        partition_keys=archives)
    return archives

@asset(
    partitions_def=password_archive_partitions_def,
    deps=[cit0day_prem_special_for_xssis_file_list]
)
def cit0day_uncompressed(context: AssetExecutionContext, s3: S3Resource):
    archive = context.partition_key
    buffer = BytesIO()

    s3.get_client().download_fileobj(SOURCE_BUCKET, archive, buffer)

    with zipfile.ZipFile(buffer, 'r') as zip_ref:
         for zip_info in zip_ref.infolist():
            if not zip_info.is_dir():
                # Read each file
                with zip_ref.open(zip_info) as file:
                    file_data = file.read()
                    file_data = file.read()

                    # Step 3: Upload each extracted file to the target MinIO/S3 bucket
                    s3.put_object(
                        Bucket=TARGET_BUCKET,
                        Key=f"{archive}/{zip_info.filename}",
                        Body=BytesIO(file_data),
                        ContentType='text/plain'
                    )
                print(f"Uploaded {zip_info.filename} to {TARGET_BUCKET}")
    
