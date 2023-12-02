import asyncio
import logging
import random
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Coroutine

from src.rema.client import RemaClient
from src.rema.json_dtos.department_dto import RemaDepartmentDto
from src.scraper import Scraper
from src.storage import DataStorage

logger = logging.getLogger(__name__)


class RemaScraper(Scraper):
    INTERVAL_MIN_SECONDS = 5
    INTERVAL_MAX_SECONDS = 20

    def __init__(
        self,
        data_storage: DataStorage,
        client: RemaClient,
        wait_func: Callable[[float], Coroutine[Any, Any, None]],
    ):
        super().__init__(data_storage)
        self._client = client
        self._data_storage = data_storage
        self._wait_func = wait_func

    async def scrape(self):
        logger.info(f"Scraping started")

        logger.info("Requesting: All departments")
        department_dtos = self._client.fetch_departments()

        total_departments = len(department_dtos)
        total_categories = sum(
            len(department.categories) for department in department_dtos
        )

        logger.info(
            f"Found {total_departments} departments and {total_categories} categories"
        )

        random.shuffle(department_dtos)

        estimated_fetch_duration, estimated_fetch_end_time = self._estimate_fetch_time(
            total_categories
        )
        logger.info(
            f"Estimated fetch time: {estimated_fetch_duration} (End time: {estimated_fetch_end_time})"
        )

        # Start scraping departments
        start_time = datetime.utcnow()
        await self._scrape_departments(department_dtos)
        end_time = datetime.utcnow()

        # logger.info(f"--Products in category: {len(categoryDto.hits)}") # TODO: print num products and see if any product requests reaches 1000
        logger.info(
            f"Done fetching data from Rema. Took {end_time - start_time} (Estimated: {estimated_fetch_duration})"
        )

    # iterate over departments and then categories in that department, then fetch products in each category
    async def _scrape_departments(self, departmentDtos: list[RemaDepartmentDto]):
        for idx, department in enumerate(departmentDtos):
            logger.info(
                f"For department {department.id}: {department.name} ({idx + 1}/{len(departmentDtos)})"
            )
            await self._scrape_categories(department)

    async def _scrape_categories(self, department: RemaDepartmentDto):
        for idx, category in enumerate(department.categories):
            logger.info(
                f"- Requesting: Category {category.id}: {category.name} ({idx + 1}/{len(department.categories)})"
            )
            category_products_json = self._client.fetch_products_json(category.id)

            file_name = f"dep_{department.id}_cat_{category.id}.json"
            logger.info(f"-- Saving to file: {file_name}")
            self._data_storage.save_data(file_name, category_products_json)
            await self._wait()

    async def _wait(self):
        wait = random.uniform(self.INTERVAL_MIN_SECONDS, self.INTERVAL_MAX_SECONDS)
        logger.info(f"Waiting {wait:.1f} seconds...")
        await self._wait_func(wait)

    def _estimate_fetch_time(self, total_categories: int):
        estimated_fetch_duration = timedelta(
            seconds=(
                total_categories
                * (self.INTERVAL_MIN_SECONDS + self.INTERVAL_MAX_SECONDS)
            )
            / 2
        )
        estimated_fetch_end_time = datetime.now(timezone.utc) + estimated_fetch_duration
        return estimated_fetch_duration, estimated_fetch_end_time
