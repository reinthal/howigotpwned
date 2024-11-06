import pyarrow as pa
from pyiceberg.catalog import Catalog
from tenacity import retry, stop_after_attempt, wait_exponential


def append_to_table_with_retry(
    pa_df: pa.Table, table_name: str, catalog: Catalog
) -> None:
    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=32),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def append_with_retry():
        table = catalog.load_table(table_name)
        table.append(pa_df)

    append_with_retry()
