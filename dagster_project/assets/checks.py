import json
import traceback

from dagster import (
    AssetCheckExecutionContext,
    AssetCheckResult,
    AssetCheckSeverity,
    asset_check,
)
from dagster_snowflake import SnowflakeResource
from pandera import Column, DataFrameSchema, errors, Int8, Int16

from dagster_project.constants import (
    snowflake_database,
    source_schema_name,
    source_base_name
)


@asset_check(asset="dlt_pokemon_pokemon")
def validate_schema_pokemon_pokemon(
    context: AssetCheckExecutionContext, snowflake: SnowflakeResource
) -> AssetCheckResult:
    schema = DataFrameSchema(
        {
            "BASE_EXPERIENCE": Column(Int16),
            "HEIGHT": Column(Int8),
            "ID": Column(Int8),
            "NAME": Column(str),
            "SPECIES__NAME": Column(str),
            "WEIGHT": Column(Int16)
        },
        # Only check columns defined in schema.
        strict=False,
        report_duplicates="all",
    )

    with snowflake.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"USE DATABASE {snowflake_database}")
            cursor.execute(f"USE SCHEMA {source_schema_name}")

            table_name = (
                context.check_specs[0]
                .asset_key.to_user_string()
                .removeprefix(f"dlt_{source_base_name}_")
            )

            cursor.execute(f"SELECT * FROM {table_name.upper()}")
            df = cursor.fetch_pandas_all()

    try:
        schema.validate(df, lazy=True)

        return AssetCheckResult(passed=True)

    except errors.SchemaErrors as e:
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.ERROR,
            metadata={"error": json.dumps(e.message, indent=2)},
        )

    except Exception as e:
        return AssetCheckResult(
            passed=False, severity=AssetCheckSeverity.ERROR, metadata={"error": str(e)}
        )


@asset_check(asset="dlt_pokemon_species")
def validate_schema_pokemon_species(
    context: AssetCheckExecutionContext, snowflake: SnowflakeResource
) -> AssetCheckResult:
    schema = DataFrameSchema(
        {
            "BASE_HAPPINESS": Column(Int8),
            "GENERATION__NAME": Column(str),
            "ID": Column(Int8),
            "IS_MYTHICAL": Column(bool),
        },
        # Only check columns defined in schema.
        strict=False,
        report_duplicates="all",
    )

    with snowflake.get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"USE DATABASE {snowflake_database}")
            cursor.execute(f"USE SCHEMA {source_schema_name}")

            table_name = (
                context.check_specs[0]
                .asset_key.to_user_string()
                .removeprefix(f"dlt_{source_base_name}_")
            )

            cursor.execute(f"SELECT * FROM {table_name.upper()} LIMIT 10")
            df = cursor.fetch_pandas_all()

    try:
        schema.validate(df, lazy=True)

        return AssetCheckResult(passed=True)

    except errors.SchemaErrors as e:
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.ERROR,
            metadata={
                "error": json.dumps(e.message, indent=2),
                "error_type": type(e).__name__,
            },
        )

    except Exception as e:
        return AssetCheckResult(
            passed=False,
            severity=AssetCheckSeverity.ERROR,
            metadata={
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc(),
            },
        )