import asyncio
import logging
import random
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Coroutine

from src.utils import get_utc_now

logger = logging.getLogger(__name__)


# Waits for a random time between min_wait and max_wait
class Waiter:
    def __init__(
        self,
        min_wait: timedelta,
        max_wait: timedelta,
        get_uniform_random: Callable[[float, float], float],
        sleep: Callable[[float], Coroutine[Any, Any, None]],
    ):
        self._validate_wait_times(min_wait, max_wait)
        self._min_wait = min_wait
        self._max_wait = max_wait
        self._random_provider = get_uniform_random
        self._sleep = sleep
        logger.info(
            f"Waiter initialized with min seconds: {min_wait} and max seconds: {max_wait}"
        )

    async def wait(self):
        wait = self._random_provider(
            self._min_wait.total_seconds(), self._max_wait.total_seconds()
        )
        logger.info(f"Waiting {wait:.1f} seconds...")
        await self._sleep(wait)

    def estimate_total_wait(self, total_calls: int) -> timedelta:
        if total_calls <= 0:
            raise ValueError("total_items must be greater than 0")

        estimated_wait_secs = (
            total_calls
            * (self._min_wait.total_seconds() + self._max_wait.total_seconds())
            / 2
        )
        estimated_wait_duration = timedelta(seconds=estimated_wait_secs)
        return estimated_wait_duration

    def _validate_wait_times(self, min_wait: timedelta, max_wait: timedelta):
        if min_wait < timedelta(seconds=0) or max_wait < timedelta(seconds=0):
            raise ValueError("min_wait and max_wait must be positive")

        if min_wait > max_wait:
            raise ValueError("min_wait must be less than or equal to max_wait")
