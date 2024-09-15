from dagster import AssetSelection, Definitions, define_asset_job

from dagster_project.assets import (
    cit0day_prem_special_for_xssis_archives,
    cit0day_uncompressed,
    cit0day_password_files,
)
from dagster_project.resources import nas_minio

# Define a job that targets asset_a and all its upstream dependencies
cit0day_job = define_asset_job(
    name="cit0day_job",
    selection=AssetSelection.assets(cit0day_prem_special_for_xssis_archives).upstream()
)


defs = Definitions(
    jobs=[cit0day_job], 
    resources={"s3": nas_minio},  
    assets=[
        cit0day_prem_special_for_xssis_archives, 
        cit0day_uncompressed,
        cit0day_password_files
    ]
)  # noqa: E501
