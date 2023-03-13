from src.rema.client import save_rema_data
import logging
import time


# Setup logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more verbose logging
    format='[%(asctime)s] [%(levelname)s] %(name)-25s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.Formatter.converter = time.gmtime  # Use UTC
logger = logging.getLogger(__name__)

# TODO: Convert to domain objects and store in database
# Save rema data to json.
save_rema_data()
