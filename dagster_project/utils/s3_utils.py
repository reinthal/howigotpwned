import os
import tempfile
from typing import Generator

import patoolib
from dagster_aws.s3 import S3Resource


def get_objects(source_bucket: str, prefix: str, s3: S3Resource) -> Generator:
    paginator = s3.get_client().get_paginator("list_objects")
    response_iterator = paginator.paginate(Bucket=source_bucket, Prefix=prefix)

    # do the paginator loop
    objs = []
    for page in iter(response_iterator):
        # loop over each page
        archives = [obj["Key"] for obj in page["Contents"]]
        objs = objs + archives
    return objs


def copy_archive_to_s3(
    s3: S3Resource, destination_bucket: str, archive_path, parent_key=""
):
    # Create filesystems
    client = s3.get_client()
    with tempfile.TemporaryDirectory() as tmpdirname:
        patoolib.extract_archive(archive_path, outdir=tmpdirname)
        for f in os.listdir(tmpdirname):
            Key = f if not parent_key else f"{parent_key}/{f}"
            client.upload_file(f"{tmpdirname}/{f}", Bucket=destination_bucket, Key=Key)


def test_copy_archive_to_s3():
    from dagster import EnvVar

    bucket_name = "dev"

    # Connect to MinIO
    nas_minio = S3Resource(
        aws_secret_access_key=EnvVar("S3_SECRET_KEY").get_value(),
        aws_access_key_id=EnvVar("S3_ACCESS_KEY").get_value(),
        endpoint_url=EnvVar("S3_ENDPOINT").get_value(),
    )
    archive_path = "/home/kog/Downloads/zipcaars.com {1.170} [HASH] (Business)_special_for_XSS.IS.rar"
    copy_archive_to_s3(nas_minio, bucket_name, archive_path=archive_path)


def test_get_objects():
    from dagster import EnvVar

    bucket_name = "dev"

    # Connect to MinIO
    nas_minio = S3Resource(
        aws_secret_access_key=EnvVar("S3_SECRET_KEY").get_value(),
        aws_access_key_id=EnvVar("S3_ACCESS_KEY").get_value(),
        endpoint_url=EnvVar("S3_ENDPOINT").get_value(),
    )

    source_bucket = "raw"
    prefix = "Cit0/Cit0day.in_special_for_xss.is/Cit0day Prem [_special_for_xss.is]/0-de-franchise.ca {6.584} [HASH+NOHASH] (NoCategory)_special_for_XSS.IS.rar"
    objs = get_objects(source_bucket=source_bucket, prefix=prefix, s3=nas_minio)
    print(len(list(objs)))


if __name__ == "__main__":
    test_get_objects()
