from dagster import AssetSelection, Definitions, ScheduleDefinition, define_asset_job

from dagster_project.assets import (
    cit0day_password_files,
    cit0day_prem_special_for_xssis_archives,
)
from dagster_project.resources import nas_minio

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
)  # noqa: E501
