import polars as pl
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.transforms import IdentityTransform
from pyiceberg.types import NestedField, StringType

cit0day_polars_schema = pl.Schema(
    {
        "email": pl.String(),
        "username": pl.String(),
        "domain": pl.String(),
        "data": pl.String(),
        "bucket": pl.String(),
        "prefix": pl.String(),
        "category": pl.String(),
    }
)
cit0day_schema = Schema(
    NestedField(field_id=1, name="email", field_type=StringType(), required=False),
    NestedField(field_id=2, name="username", field_type=StringType(), required=False),
    NestedField(field_id=3, name="domain", field_type=StringType(), required=False),
    NestedField(field_id=4, name="data", field_type=StringType(), required=False),
    NestedField(field_id=5, name="bucket", field_type=StringType(), required=False),
    NestedField(field_id=6, name="prefix", field_type=StringType(), required=False),
    NestedField(field_id=7, name="category", field_type=StringType(), required=False),
)

cit0day_partition_spec = PartitionSpec(
    PartitionField(
        source_id=3,  # field_id for domain
        field_id=1000,  # new field_id for partition field
        transform=IdentityTransform(),
        name="domain",
    ),
    PartitionField(
        source_id=7,  # field_id for category
        field_id=1001,  # new field_id for partition field
        transform=IdentityTransform(),
        name="category",
    ),
)
