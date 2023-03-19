from datetime import datetime, timezone


# get utc now timezone aware
def get_utc_now():
    return datetime.now(timezone.utc)