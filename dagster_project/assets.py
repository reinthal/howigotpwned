from typing import Any
from dagster import asset
from dagster_aws.s3 import S3Resource


@asset
def cit0day_prem_special_for_xssis_file_list(s3: S3Resource) -> Any:
    """All password dumps and puts in minio"""
    return s3.get_client().list_objects(Bucket="leaks", Marker="Cit0/Cit0day.in_special_for_xss.is/Cit0day Prem [_special_for_xss.is]")
