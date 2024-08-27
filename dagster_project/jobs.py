from dagster import define_asset_job, AssetSelection

from dagster_project.assets.assets import pokemon_assets
from .constants import source_base_name

pokemon_job = define_asset_job(
    name=f"{source_base_name}_job",
    selection=AssetSelection.assets(pokemon_assets).downstream(),
    description="",
)
