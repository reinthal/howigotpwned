from typing import Any
from dagster import job, op, Definitions, asset, EnvVar
from dagster_aws.s3 import S3Resource

nas_minio = S3Resource(
    aws_secret_access_key=EnvVar("S3_SECRET_KEY"),
    aws_access_key_id=EnvVar("S3_ACCESS_KEY"),
    endpoint_url=EnvVar("S3_ENDPOINT"),
)


@op
def example_s3_op(s3: S3Resource):
    return s3.get_client().list_objects_v2(Bucket="leaks")


@job
def example_job():
    example_s3_op()


defs = Definitions(jobs=[example_job], resources={"s3": nas_minio})


@asset
def password_dumps_rar(s3: S3Resource = nas_minio) -> Any:
    """All password dumps and puts in minio"""
    return s3.get_client.list_objects(Bucket="leaks")
