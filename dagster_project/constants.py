from dagster import EnvVar

source_base_name = "pokemon"
snowflake_database = EnvVar("DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE").get_value()
source_schema_name = f"raw_{source_base_name}"