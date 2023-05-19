import asyncio
import logging

import src.utils as utils
from src.rema.rema_scraper import scrape_and_save_rema

logger = logging.getLogger(__name__)


async def main():
    # Save rema data to json.
    await scrape_and_save_rema()


if __name__ == "__main__":
    try:
        utils.setup_logging()
        asyncio.run(main())
    except Exception as e:
        raise Exception(f"Unhandled exception occurred: {e}") from e
