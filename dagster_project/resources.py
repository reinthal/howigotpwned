from dagster import EnvVar

from dagster_aws.s3 import S3Resource

nas_minio = S3Resource(
    aws_secret_access_key=EnvVar("S3_SECRET_KEY"),
    aws_access_key_id=EnvVar("S3_ACCESS_KEY"),
    endpoint_url=EnvVar("S3_ENDPOINT"),
)


