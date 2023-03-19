from pathlib import Path
from src.rema.client import save_rema_data
import logging
import time
import asyncio
import argparse
from dotenv import load_dotenv
from os import environ as env
from src.discord_webhook import notify_exception

# Setup logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more verbose logging
    format='[%(asctime)s] [%(levelname)s] %(name)-25s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logging.Formatter.converter = time.gmtime  # Use UTC
logger = logging.getLogger(__name__)


ap = argparse.ArgumentParser()
ap.add_argument("-e", "--env", required=False, type=str,
                help="Path of .env file", default=".env")
args = vars(ap.parse_args())

env_path = args["env"]
if not Path(env_path).exists() or not Path(env_path).is_file():
    raise IOError(f"No .env file found at path: '{env_path}'")
else:
    logging.info(f"Loading .env file from path: '{env_path}'")

load_dotenv(dotenv_path=args["env"])



# TODO: Convert to domain objects and store in database
async def main():
    # Save rema data to json.
    await save_rema_data()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        webhook_url = env['DISCORD_ERROR_WEBHOOK']
        # notify
        notify_exception(webhook_url, e, "supermarket-price-tracker")
        raise Exception(f"Unhandled exception occurred: {e}") from e