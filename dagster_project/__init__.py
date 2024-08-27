from dagster import Definitions, load_assets_from_package_module, load_asset_checks_from_package_module
from dagster_project.resources import snowflake_resource, dlt_resource
from dagster_project.jobs import pokemon_job
from dagster_project.schedules import pokemon_schedule
from dagster_project import assets

all_assets = load_assets_from_package_module(assets)
all_checks = load_asset_checks_from_package_module(assets)

# Definitions
defs = Definitions(
    assets=all_assets,
    asset_checks=all_checks,
    jobs=[pokemon_job],
    schedules=[pokemon_schedule],
    resources={
        "snowflake": snowflake_resource,
        "dlt": dlt_resource,
    },
)
