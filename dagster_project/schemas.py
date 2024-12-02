import polars as pl
from pyiceberg.partitioning import PartitionField, PartitionSpec
from pyiceberg.schema import Schema
from pyiceberg.table.sorting import SortField, SortOrder
from pyiceberg.transforms import IdentityTransform
from pyiceberg.types import DateType, NestedField, StringType

cit0day_polars_schema = pl.Schema(
    {
        "email": pl.String(),
        "username": pl.String(),
        "email_domain": pl.String(),
        "data": pl.String(),
        "bucket": pl.String(),
        "prefix": pl.String(),
        "category": pl.String(),
        "date":  pl.Date()
    }
)
# Add a cit0day schema
cit0day_schema = Schema(
    NestedField(field_id=1, name="email", field_type=StringType(), required=False),
    NestedField(field_id=2, name="username", field_type=StringType(), required=False),
    NestedField(
        field_id=3, name="email_domain", field_type=StringType(), required=False
    ),
    NestedField(field_id=4, name="data", field_type=StringType(), required=False),
    NestedField(field_id=5, name="bucket", field_type=StringType(), required=False),
    NestedField(field_id=6, name="prefix", field_type=StringType(), required=False),
    NestedField(field_id=7, name="category", field_type=StringType(), required=False),
    NestedField(field_id=7, name="date", field_type=DateType(), required=False),
)


# Define the index mappings
passwords_mappings = {
    "mappings": {
        "properties": {
            "email": {
                "type": "text",  # or "keyword" if you want exact matches
            },
            "username": {
                "type": "keyword",
            },
            "email_domain": {
                "type": "keyword",  # or "keyword" if you want exact matches
            },
            "data": {
                "type": "keyword",
                "index": False 
            },
            "bucket": {
                "type": "keyword",  # or "keyword" if you want exact matches
                "index": False 
            },
            "prefix": {
                "type": "keyword",  # or "keyword" if you want exact matches
                "index": False 
            },
            "category": {
                "type": "keyword",  # keyword will be better for exact matches
            },
            "date": {
                "type": "date",
                "index": False 
                
            }
        }
    }
}

cit0day_sort_order = SortOrder(SortField(source_id=1, transform=IdentityTransform()))

cit0day_partition_spec = PartitionSpec(
    PartitionField(
        source_id=7,  # field_id for category
        field_id=1001,  # new field_id for partition field
        transform=IdentityTransform(),
        name="category",
    ),
)
