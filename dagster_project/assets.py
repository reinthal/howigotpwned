from typing import Any
from dagster import asset
from dagster_aws.s3 import S3Resource


@asset
def password_dumps_rar(s3: S3Resource) -> Any:
    """All password dumps and puts in minio"""
    return s3.get_client.list_objects(Bucket="leaks")
