from io import BytesIO

import polars as pl


def create_passwords_polars_frame_from_file(
    bytes_io: BytesIO, schema: pl.Schema
) -> pl.DataFrame:
    # Prepare lists to store each column data
    emails = []
    usernames = []
    domains = []
    data = []

    # Open the file and process each line
    bytes_io.seek(0)
    for line in bytes_io:
        try:
            line = line.decode("utf-8")
        except UnicodeDecodeError:
            line = line.decode("latin-1")
        # Strip newline characters and split only on the first occurrence of :
        parts = line.strip().split(":", 1)
        
        email, datum = parts
        # Get the username and domain of the email
        username, domain = email.strip().split("@", 1)
        emails.append(email)
        usernames.append(username)
        domains.append(domain)
        data.append(datum)

    # Create a Polars DataFrame
    df = pl.DataFrame(
        {
            "email": emails,
            "username": usernames,
            "domain": domains,
            "data": data,
            "bucket": [None for _ in range(0, len(emails))],
            "prefix": [None for _ in range(0, len(data))],
        },
        schema=schema,
    )

    return df
