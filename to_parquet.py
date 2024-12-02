import os
import re
import uuid
from pathlib import Path

import polars as pl
from tqdm import tqdm

from dagster_project.schemas import (
    cit0day_polars_schema,
)
from dagster_project.utils.passwords import create_passwords_polars_frame_from_file

CATEGORY_REGEX = r".*\((?P<category>.*?)\)"
RAW_BUCKET = "raw"
FOLDER_PATH = "extracted"

source_directory = "/mnt/data/kog/Cit0day Prem [_special_for_xss.is]/"
destination_directory = "/mnt/data/kog/parquetes/"

source_directory = Path("/mnt/data/kog/Cit0day Prem [_special_for_xss.is]/")
file_paths = list(source_directory.rglob("*"))  # rglob is recursive glob

file_paths = [str(f) for f in file_paths if os.path.isfile(f)]

# Ensure the destination directory exists
os.makedirs(destination_directory, exist_ok=True)
# Generating a UUID4
unique_id = uuid.uuid4()


def main():
    dfs = pl.DataFrame(schema=cit0day_polars_schema)
    for obj in tqdm(file_paths, desc="Processing files"):
        print(obj)
        # - file name
        file_name = obj
        # open the file
        with open(file_name, "rb") as file_obj:
            df = create_passwords_polars_frame_from_file(
                file_obj, cit0day_polars_schema
            )

            match = re.search(CATEGORY_REGEX, file_name)
            if match:
                category = match.group("category")
            else:
                category = "no category"

            df = df.with_columns(
                (pl.lit(RAW_BUCKET)).alias("bucket"),
                (pl.lit(file_name)).alias("prefix"),
                (pl.lit(category).alias("category")),
            )
            if dfs.estimated_size("mb") > 300.0:
                uid = uuid.uuid4()  # Define how to generate a unique identifier
                output_file = os.path.join(destination_directory, f"{uid}.parquet")
                dfs.write_parquet(output_file)
                print(f"Data written to {output_file} and DataFrame reset.")
                dfs = pl.DataFrame(schema=cit0day_polars_schema)  # Reset the DataFrame
            else:
                dfs = pl.concat([dfs, df])


if __name__ == "__main__":
    main()
