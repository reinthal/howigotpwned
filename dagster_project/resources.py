from dagster import EnvVar
from dagster_aws.s3 import S3Resource
from dagster import asset, Definitions, ConfigurableResource
from pyiceberg.catalog import load_catalog, Catalog


class NessieCatalogResource(ConfigurableResource):
    name: str = "default"
    warehouse: str
    branch: str
    uri: str
    py_io_impl: str = "pyiceberg.io.pyarrow.PyArrowFileIO"
    s3_endpoint: str
    s3_access_key_id: str
    s3_secret_access_key: str
    catalog_type: str = "rest"

    def get_catalog(self) -> Catalog:
        return load_catalog(
            self.name,
            **{
                "warehouse": self.warehouse,
                "uri": f"{self.uri}/{self.branch}",
                "py-io-impl": self.py_io_impl,
                "s3.endpoint": self.s3_endpoint,
                "s3.access-key-id": self.s3_access_key_id,
                "s3.secret-access-key": self.s3_secret_access_key,
                "type": self.catalog_type,
            },
        )


nas_minio = S3Resource(
    aws_secret_access_key=EnvVar(
        "SOURCES__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"
    ),
    aws_access_key_id=EnvVar("SOURCES__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"),
    endpoint_url=EnvVar("SOURCES__FILESYSTEM__CREDENTIALS__AWS_S3_ENDPOINT"),
)
