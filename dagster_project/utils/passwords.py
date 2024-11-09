from io import BytesIO

import polars as pl


def create_passwords_polars_frame_from_file(
    bytes_io: BytesIO, schema: pl.Schema
) -> pl.DataFrame:
    # Prepare lists to store each column data
    emails = []
    usernames = []
    email_domains = []
    data = []

    # Open the file and process each line
    bytes_io.seek(0)
    for line in bytes_io:
        try:
            line = line.decode("utf-8")
        except UnicodeDecodeError:
            line = line.decode("latin-1")

        email = line
        datum = ""
        username = ""
        domain = ""

        # Strip newline characters and split only on the first occurrence of :
        parts = line.strip().split(":", 1)
        if len(parts) == 2:
            email, datum = parts
            parts2 = email.strip().split("@", 1)

            if len(parts2) == 2:
                # Get the username and domain of the email
                username, domain = parts2

        emails.append(email)
        usernames.append(username)
        email_domains.append(domain)
        data.append(datum)

    # Create a Polars DataFrame
    df = pl.DataFrame(
        {
            "email": emails,
            "username": usernames,
            "email_domain": email_domains,
            "data": data,
            "bucket": [None for _ in range(0, len(data))],
            "prefix": [None for _ in range(0, len(data))],
            "category": [None for _ in range(0, len(data))],
        },
        schema=schema,
    )

    return df
