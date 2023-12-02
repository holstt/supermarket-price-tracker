import asyncio
import logging
from pathlib import Path

import src.utils as utils
from src.rema.client import RemaClient
from src.rema.scraper import RemaScraper
from src.storage import DataStorage

logger = logging.getLogger(__name__)


async def main():
    base_dir = Path("data")
    STORE_NAME = "rema"
    client = RemaClient()
    storage = DataStorage(base_dir, STORE_NAME)
    scraper = RemaScraper(storage, client, asyncio.sleep)
    await scraper.scrape()


if __name__ == "__main__":
    try:
        utils.setup_logging()
        asyncio.run(main())
    except Exception as e:
        raise Exception(f"Unhandled exception occurred: {e}") from e
