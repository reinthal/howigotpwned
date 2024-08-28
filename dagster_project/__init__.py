from dagster import Definitions
from dagster_project.resources import nas_minio
from dagster_project.assets import password_dumps_rar


defs = Definitions(jobs=[], resources={"s3": nas_minio}, assets=[password_dumps_rar])
