from dagster import DynamicPartitionsDefinition

password_archive_partitions_def = DynamicPartitionsDefinition(name="password_archives")
