from dagster import Definitions

from dagster_project.assets import (
    cit0day_password_files,
    cit0day_prem_special_for_xssis_archives,
)
from dagster_project.jobs import cit0day_job
from dagster_project.k8s_config import job_executor
from dagster_project.resources import nas_minio, nessie_default_catalog
from dagster_project.utils.environment import is_local_environment

defs = Definitions(
    jobs=[cit0day_job],
    schedules=[],
    resources={
        "s3": nas_minio,
        "nessie_default": nessie_default_catalog,
    },
    assets=[cit0day_prem_special_for_xssis_archives, cit0day_password_files],
    executor=None if is_local_environment() else job_executor,
)  # noqa: E501
