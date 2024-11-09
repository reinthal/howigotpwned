from dagster import (
    AssetSelection,
    Definitions,
    define_asset_job,
)

from dagster_project.utils.environment import is_local_environment
from dagster_project.assets import (
    cit0day_password_files,
    cit0day_prem_special_for_xssis_archives,
)
from dagster_k8s import k8s_job_executor
from dagster_project.resources import nas_minio, nessie_default_catalog


job_executor = k8s_job_executor.configured(
    {
        "step_k8s_config": {
            "container_config": {
                "resources": {
                    "requests": {"cpu": "2", "memory": "2Gi"},
                }
            }
        },
        "max_concurrent": 20,
    }
)

# Define a job that targets asset_a and all its upstream dependencies
cit0day_job = define_asset_job(
    name="cit0day_job",
    selection=AssetSelection.assets(
        cit0day_prem_special_for_xssis_archives
    ).downstream(),
)
cit0day_job = cit0day_job.with_tags(
    {
        "dagster-k8s/config": {
            "job_spec_config": {"ttl_seconds_after_finished": 60}  # Set TTL to 1 minute
        }
    }
)

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
