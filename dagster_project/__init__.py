from dagster import AssetSelection, Definitions, ScheduleDefinition, define_asset_job
from dagster_k8s import k8s_job_executor

from dagster_project.assets import (
    cit0day_password_files,
    cit0day_prem_special_for_xssis_archives,
)
from dagster_project.resources import nas_minio
from dagster_project.utils.environment import is_local_environment

job_executor = k8s_job_executor.configured(
    {
        "step_k8s_config": {
            "container_config": {
                "resources": {
                    "requests": {"cpu": "2", "memory": "2Gi"},
                }
            }
        }
    }
)
cit0day_schedule = ScheduleDefinition(
    name="cit0day_daily_schedule",
    cron_schedule="0 3 * * *",
    job_name="cit0day_job",
    execution_timezone="UTC",
)

# Define a job that targets asset_a and all its upstream dependencies
cit0day_job = define_asset_job(
    name="cit0day_job",
    selection=AssetSelection.assets(cit0day_prem_special_for_xssis_archives).upstream(),
)


defs = Definitions(
    jobs=[cit0day_job],
    schedules=[cit0day_schedule],
    resources={"s3": nas_minio},
    assets=[cit0day_prem_special_for_xssis_archives, cit0day_password_files],
    executor=None if is_local_environment() else job_executor,
)  # noqa: E501
