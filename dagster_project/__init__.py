from dagster import (
    AssetSelection,
    Definitions,
    define_asset_job,
)

from dagster_project.assets import (
    cit0day_password_files,
    cit0day_prem_special_for_xssis_archives,
)
from dagster_project.resources import nas_minio, nessie_default_catalog

# Define a job that targets asset_a and all its upstream dependencies
cit0day_job = define_asset_job(
    name="cit0day_job",
    selection=AssetSelection.assets(
        cit0day_prem_special_for_xssis_archives
    ).downstream(),
)


defs = Definitions(
    jobs=[cit0day_job],
    schedules=[],
    resources={
        "s3": nas_minio,
        "nessie_default": nessie_default_catalog,
    },
    assets=[cit0day_prem_special_for_xssis_archives, cit0day_password_files],
    executor=None,
)  # noqa: E501
