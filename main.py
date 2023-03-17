from src.rema.client import save_rema_data
import logging
import time
import asyncio

# Setup logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more verbose logging
    format='[%(asctime)s] [%(levelname)s] %(name)-25s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.Formatter.converter = time.gmtime  # Use UTC
logger = logging.getLogger(__name__)

# TODO: Convert to domain objects and store in database
async def main():
    # Save rema data to json.
    await save_rema_data()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        raise Exception(f"Unhandled exception occurred: {e}") from e