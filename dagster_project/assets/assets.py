from typing import Iterable
from dlt import pipeline
from dlt.extract.resource import DltResource
from dlt.destinations import snowflake
from dagster import AssetExecutionContext, AssetKey, SourceAsset
from dagster_embedded_elt.dlt import DagsterDltResource, DagsterDltTranslator, dlt_assets
from data_sources.pokemon import pokemon

from ..constants import (
    source_base_name,
    source_schema_name,
)


pipeline_name = f"{source_base_name}_dlt_pipeline"


class DltPipelineTranslator(DagsterDltTranslator):
    """inspired by: https://github.com/dagster-io/dagster/issues/21049#issuecomment-2043147862"""

    def get_deps_asset_keys(self, resource: DltResource) -> Iterable[AssetKey]:
        return [AssetKey([pipeline_name])]


@dlt_assets(
    dlt_source=pokemon(),
    dlt_pipeline=pipeline(
        pipeline_name=pipeline_name,
        dataset_name=source_schema_name,
        destination=snowflake(),
        progress="enlighten",
    ),
    name=f"{source_base_name}",
    group_name=f"{source_base_name}",
    dagster_dlt_translator=DltPipelineTranslator()
)
def pokemon_assets(context: AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

    
"""
Modifies metadata group name for the dlt_assets 
to have depedencies in same group as assets.
SourceAsset is deprecated but this does not work with AssetSpec yet.
"""
pokemon_assets_source = [
    SourceAsset(
        key=key, 
        group_name=source_base_name, 
        description=f"Dlt pipeline to load {source_base_name.capitalize()} data into {snowflake.__name__.capitalize()}."
        ) 
    for key in pokemon_assets.dependency_keys
    ]
