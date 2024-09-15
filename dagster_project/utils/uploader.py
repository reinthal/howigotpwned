import os
from dagster import EnvVar
import patoolib
import tempfile
from dagster_aws.s3 import S3Resource


def copy_archive_to_s3(s3: S3Resource, destination_bucket: str, archive_path, parent_key=""):
    # Create filesystems
    client = s3.get_client()
    with tempfile.TemporaryDirectory() as tmpdirname:
        patoolib.extract_archive(archive_path, outdir=tmpdirname)
        for f in os.listdir(tmpdirname):
            Key = f if not parent_key else f"{parent_key}/{f}"
            client.upload_file(f"{tmpdirname}/{f}", Bucket=destination_bucket, Key=Key)

def main():
    bucket_name = 'dev'

    # Connect to MinIO
    nas_minio = S3Resource(
        aws_secret_access_key=EnvVar("S3_SECRET_KEY").get_value(),
        aws_access_key_id=EnvVar("S3_ACCESS_KEY").get_value(),
        endpoint_url=EnvVar("S3_ENDPOINT").get_value(),
    )
    archive_path = "/home/kog/Downloads/zipcaars.com {1.170} [HASH] (Business)_special_for_XSS.IS.rar"
    copy_archive_to_s3(nas_minio, bucket_name, archive_path=archive_path)

    
    

if __name__ == '__main__':
    main()