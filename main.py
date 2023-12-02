import asyncio
import logging
from pathlib import Path

import src.utils as utils
from src.rema.client import RemaClient
from src.rema.scraper import RemaScraper
from src.storage import DataStorage
from src.waiter import Waiter

logger = logging.getLogger(__name__)


async def main():
    INTERVAL_MIN_SECONDS = 5
    INTERVAL_MAX_SECONDS = 20
    STORE_NAME = "rema"
    DATA_PATH = "./data"

    base_dir = Path(DATA_PATH)
    client = RemaClient()
    storage = DataStorage(base_dir, STORE_NAME)
    waiter = Waiter(INTERVAL_MIN_SECONDS, INTERVAL_MAX_SECONDS)
    scraper = RemaScraper(storage, client, waiter)
    await scraper.scrape()


if __name__ == "__main__":
    try:
        utils.setup_logging()
        asyncio.run(main())
    except Exception as e:
        raise Exception(f"Unhandled exception occurred: {e}") from e
