import logging
import time
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


# get utc now timezone aware
def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


def setup_logging():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(name)-25s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.Formatter.converter = time.gmtime  # Use UTC
