from dagster import ScheduleDefinition, DefaultScheduleStatus
from dagster_project.jobs import pokemon_job

pokemon_schedule = ScheduleDefinition(
    job=pokemon_job,
    # Run on weekdays 1-5 @ 15:05
    cron_schedule="15 5 * * 1-5",
    default_status=DefaultScheduleStatus.RUNNING,
)
