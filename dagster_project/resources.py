from dagster import ConfigurableResource, EnvVar
from dagster_aws.s3 import S3Resource
from pyiceberg.catalog import Catalog, load_catalog


class ElasticResource(ConfigurableResource):
    url: str = "https://elastic.local.reinthal.cc"
    username: str = EnvVar("ELASTIC_USERNAME")
    password: str = EnvVar("ELASTIC_PASSWORD")
    password_index: str = EnvVar("ELASTIC_PASSWORD_INDEX")

class NessieCatalogResource(ConfigurableResource):
    name: str = "default"
    warehouse: str = EnvVar("NESSIE_WAREHOUSE")
    branch: str = EnvVar("NESSIE_BRANCH")
    uri: str = EnvVar("NESSIE_URI")
    py_io_impl: str = "pyiceberg.io.pyarrow.PyArrowFileIO"
    s3_endpoint: str = EnvVar("DESTINATION__FILESYSTEM__CREDENTIALS__AWS_S3_ENDPOINT")
    s3_access_key_id: str = EnvVar(
        "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"
    )
    s3_secret_access_key: str = EnvVar(
        "DESTINATION__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"
    )
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


nessie_default_catalog = NessieCatalogResource()
elastic = ElasticResource()
nas_minio = S3Resource(
    aws_secret_access_key=EnvVar(
        "SOURCES__FILESYSTEM__CREDENTIALS__AWS_SECRET_ACCESS_KEY"
    ),
    aws_access_key_id=EnvVar("SOURCES__FILESYSTEM__CREDENTIALS__AWS_ACCESS_KEY_ID"),
    endpoint_url=EnvVar("SOURCES__FILESYSTEM__CREDENTIALS__AWS_S3_ENDPOINT"),
)
