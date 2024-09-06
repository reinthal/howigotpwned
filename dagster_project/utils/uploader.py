import os
from dagster import EnvVar
import patoolib
import tempfile
from dagster_aws.s3 import S3Resource

class Uploader:

    def __init__(self, s3: S3Resource, bucket: str):
        self.s3 = s3
        self.bucket = bucket
    
    def copy_archive_to_s3(self, archive_path, parent_key=""):
        # Create filesystems
        client = self.s3.get_client()
        with tempfile.TemporaryDirectory() as tmpdirname:
            patoolib.extract_archive(archive_path, outdir=tmpdirname)
            for f in os.listdir(tmpdirname):
                print(f"{tmpdirname}/{f}")
                Key = f if not parent_key else f"{parent_key}/{f}"
                client.upload_file(f"{tmpdirname}/{f}", Bucket=self.bucket, Key=Key)

def main():
    bucket_name = 'dev'

    # Connect to MinIO
    nas_minio = S3Resource(
        aws_secret_access_key=EnvVar("S3_SECRET_KEY").get_value(),
        aws_access_key_id=EnvVar("S3_ACCESS_KEY").get_value(),
        endpoint_url=EnvVar("S3_ENDPOINT").get_value(),
    )
    ul = Uploader(nas_minio,bucket_name)
    archive_path = "/home/kog/Downloads/zipcaars.com {1.170} [HASH] (Business)_special_for_XSS.IS.rar"
    ul.copy_archive_to_s3(archive_path=archive_path)

    
    

if __name__ == '__main__':
    main()