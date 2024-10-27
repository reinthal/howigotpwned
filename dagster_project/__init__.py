from dagster import (
    AssetSelection,
    Definitions,
    EnvVar,
    ScheduleDefinition,
    define_asset_job,
)
from dagster_k8s import k8s_job_executor

from dagster_project.assets import (
    cit0day_password_files,
    cit0day_prem_special_for_xssis_archives,
)
from dagster_project.resources import NessieCatalogResource, nas_minio
from dagster_project.utils.environment import is_local_environment

job_executor = k8s_job_executor.configured(
    {
        "step_k8s_config": {
            "container_config": {
                "resources": {
                    "requests": {"cpu": "2", "memory": "2Gi"},
                }
            }
        },
        "max_concurrent": 5,  # Set your desired limit here
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
    selection=AssetSelection.assets(
        cit0day_prem_special_for_xssis_archives
    ).downstream(),
)


defs = Definitions(
    jobs=[cit0day_job],
    schedules=[cit0day_schedule],
    resources={
        "s3": nas_minio,
        "nessie_default": NessieCatalogResource(
            branch=EnvVar("NESSIE_BRANCH"),
            warehouse=EnvVar("NESSIE_WAREHOUSE"),
            uri=EnvVar("NESSIE_URI"),
            s3_endpoint=EnvVar("DESTINATION__FILESYSTEM__CREDENTIALS__AWS_S3_ENDPOINT"),
            s3_access_key_id=EnvVar(
                "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"
            ),
            s3_secret_access_key=EnvVar(
                "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"
            ),
        ),
    },
    assets=[cit0day_prem_special_for_xssis_archives, cit0day_password_files],
    executor=None if is_local_environment() else job_executor,
)  # noqa: E501
