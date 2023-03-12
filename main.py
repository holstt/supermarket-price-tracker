from src.rema.client import get_rema_data
import logging
import time


# Setup logging
logging.basicConfig(
    level=logging.NOTSET,
    format='[%(asctime)s] [%(levelname)s] %(name)-25s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.Formatter.converter = time.gmtime  # Use UTC
logger = logging.getLogger(__name__)


get_rema_data()
