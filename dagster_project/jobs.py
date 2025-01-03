from dagster import (
    AssetSelection,
    define_asset_job,
)

from dagster_project.assets import cit0day_password_files
from dagster_project.k8s_config import job_ttl

cit0day_job = define_asset_job(
    name="cit0day_job",
    tags=job_ttl,
    selection=AssetSelection.assets(cit0day_password_files),
)
