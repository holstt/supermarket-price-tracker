import asyncio
import logging
import random
from datetime import datetime, timedelta, timezone

from src.utils import get_utc_now

logger = logging.getLogger(__name__)


# Waits for a random time between min and max seconds
class Waiter:
    def __init__(self, min_seconds: float, max_seconds: float):
        self._min_seconds = min_seconds
        self._max_seconds = max_seconds
        logger.info(
            f"Waiter initialized with min seconds: {min_seconds} and max seconds: {max_seconds}"
        )

    async def wait(self):
        wait = random.uniform(self._min_seconds, self._max_seconds)
        logger.info(f"Waiting {wait:.1f} seconds...")
        await asyncio.sleep(wait)

    def estimate_total_wait(self, total_items: int) -> tuple[timedelta, datetime]:
        estimated_wait_secs = total_items * (self._min_seconds + self._max_seconds) / 2
        estimated_wait_duration = timedelta(seconds=estimated_wait_secs)
        estimated_wait_end_time = get_utc_now() + estimated_wait_duration
        return estimated_wait_duration, estimated_wait_end_time
