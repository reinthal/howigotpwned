from dagster import EnvVar
from dagster_aws.s3 import S3Resource

nas_minio = S3Resource(
    aws_secret_access_key=EnvVar(
        "SOURCES__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"
    ),
    aws_access_key_id=EnvVar("SOURCES__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"),
    endpoint_url=EnvVar("SOURCES__FILESYSTEM__CREDENTIALS__AWS_S3_ENDPOINT"),
)
