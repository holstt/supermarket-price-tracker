import asyncio
import json
import logging
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

import requests

from src.rema.json_dtos.department_dto import (
    RemaDepartmentDto,
    departments_dto_from_json,
)

logger = logging.getLogger(__name__)

# Rema API reverse engineered from their website shop:
# - Department URL returns all departments each with a list of category ids
# - Category URL returns all products in a specific category given a category id
# As such we need to fetch all departments to get the category ids, then fetch all products in each category

URL_DEPARTMENTS = "https://cphapp.rema1000.dk/api/v1/catalog/store/1/departments-v2"
URL_CATEGORY = "https://flwdn2189e-dsn.algolia.net/1/indexes/aws-prod-products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.21.1&x-algolia-application-id=FLWDN2189E&x-algolia-api-key=fa20981a63df668e871a87a8fbd0caed"
INTERVAL_MIN_SECONDS = 5
INTERVAL_MAX_SECONDS = 20
NAME = "rema"
base_dir = Path("data")


# Saves all rema data to json files
async def scrape_and_save_rema():
    logger.info(f"Data scraping started for supermaket: {NAME}")

    data_folder_path = Path(
        base_dir, NAME, datetime.utcnow().strftime("%Y-%m-%d__%H-%M-%S")
    )
    data_folder_path.mkdir(parents=True, exist_ok=False)
    logger.info(f"Created data directory for this run: {data_folder_path}")

    logger.info("Requesting: All departments")
    departmentDtos = _fetch_departments()

    total_departments = len(departmentDtos)
    total_categories = sum(len(department.categories) for department in departmentDtos)

    logger.info(
        f"Found {total_departments} departments and {total_categories} categories"
    )

    random.shuffle(departmentDtos)

    estimated_fetch_duration = timedelta(
        seconds=(total_categories * (INTERVAL_MIN_SECONDS + INTERVAL_MAX_SECONDS)) / 2
    )
    estimated_fetch_end_time = datetime.utcnow() + estimated_fetch_duration

    logger.info(
        f"Estimated fetch time: {estimated_fetch_duration} (End time: {estimated_fetch_end_time})"
    )

    start_time = datetime.utcnow()

    await scrape_departments(data_folder_path, departmentDtos)

    # logger.info(f"--Products in category: {len(categoryDto.hits)}") # TODO: print num products and see if any product requests reaches 1000
    end_time = datetime.utcnow()
    logger.info(
        f"Done fetching data from Rema. Took {end_time - start_time} (Estimated: {estimated_fetch_duration})"
    )


# iterate over departments and then categories in that department, then fetch products in each category
async def scrape_departments(
    data_folder_path: Path, departmentDtos: list[RemaDepartmentDto]
):
    for idx, department in enumerate(departmentDtos):
        logger.info(
            f"For department {department.id}: {department.name} ({idx + 1}/{len(departmentDtos)})"
        )
        for idx, category in enumerate(department.categories):
            logger.info(
                f"- Requesting: Category {category.id}: {category.name} ({idx + 1}/{len(department.categories)})"
            )
            categoryJson = _fetch_products_json(category.id)
            file_path = data_folder_path / f"dep_{department.id}_cat_{category.id}.json"
            logger.info(f"-- Saving to file: {file_path}")
            with open(file_path, "w") as f:
                json.dump(categoryJson, f)
            wait = random.uniform(INTERVAL_MIN_SECONDS, INTERVAL_MAX_SECONDS)
            logger.info(f"Waiting {wait:.1f} seconds...")
            await asyncio.sleep(wait)


# Example category: 655370
# Returns a json response with all products in a category
def _fetch_products_json(category_id: int):
    body = {
        "params": "query",
        "hitsPerPage": 1000,
        "facets": ["labels"],
        "facetFilters": [f"category_id:{category_id}"],
    }

    response = requests.post(URL_CATEGORY, json=body)
    response.raise_for_status()
    json = response.json()

    return json

    # TODO: Convert json response to dtos
    # category: CategoryDto = category_dto_from_dict(json)

    # return category


def _fetch_departments():
    response = requests.get(URL_DEPARTMENTS)
    response.raise_for_status()

    json = response.json()

    # Convert json response to dtos
    departmentDtos: list[RemaDepartmentDto] = departments_dto_from_json(json)

    return departmentDtos
