import os


def is_local_environment() -> bool:
    """Returns true if local environment is set."""
    try:
        os.environ["LOCAL_DEVELOPMENT"]
    except KeyError:
        return False
    else:
        return True
