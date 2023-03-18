import logging
from pathlib import Path
import random
from time import sleep
import requests
from src.rema.json_dtos.category_dto import CategoryDto, category_dto_from_dict
from src.rema.json_dtos.department_dto import DepartmentCategoryDto, RemaDepartmentDto, departments_dto_from_json
import json
from datetime import datetime, timedelta
import asyncio

# Rema API reverse engineered from their website shop:
# - Department URL returns all departments each with a list of category ids
# - Category URL returns all products in a specific category given a category id
# As such we need to fetch all departments to get the category ids, then fetch all products in each category

URL_DEPARTMENTS = "https://cphapp.rema1000.dk/api/v1/catalog/store/1/departments-v2"
# Api key is Rema not ours
URL_CATEGORY = "https://flwdn2189e-dsn.algolia.net/1/indexes/aws-prod-products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.21.1&x-algolia-application-id=FLWDN2189E&x-algolia-api-key=fa20981a63df668e871a87a8fbd0caed"

# Avoid being rate limited by waiting a random interval between requests

INTERVAL_MIN_SECONDS = 5
INTERVAL_MAX_SECONDS = 20

NAME = "rema"

# saves all rema data to json files
async def save_rema_data():
    logging.info(f"Data scraping started for: {NAME}")
    # Create folder for data
    data_folder_path = Path("data", NAME, datetime.utcnow().strftime("%Y-%m-%d__%H-%M-%S"))
    data_folder_path.mkdir(parents=True, exist_ok=False)
    logging.info(f"Created folder for data: {data_folder_path}")

    logging.info("Requesting: All departments")
    departmentDtos = _fetch_departments()

    total_departments = len(departmentDtos)
    total_categories = sum(len(department.categories) for department in departmentDtos)

    logging.info(
        f"Found {total_departments} departments and {total_categories} categories")

    random.shuffle(departmentDtos)

    estimated_fetch_duration =  timedelta(seconds=(total_categories * (INTERVAL_MIN_SECONDS + INTERVAL_MAX_SECONDS)) / 2)
    estimated_fetch_end_time = datetime.utcnow() + estimated_fetch_duration

    logging.info(f"Estimated fetch time: {estimated_fetch_duration} (End time: {estimated_fetch_end_time})")

    start_time = datetime.utcnow()

    # iterate over departments and categories, then fetch products in each category
    for idx, department in enumerate(departmentDtos):
        logging.info(
            f"For department {department.id}: {department.name} ({idx + 1}/{len(departmentDtos)})")
        for idx, category in enumerate(department.categories):
            logging.info(
                f"- Requesting: Category {category.id}: {category.name} ({idx + 1}/{len(department.categories)})")
            categoryJson: dict = _fetch_products_json(category.id)
            file_path = data_folder_path / f"dep_{department.id}_cat_{category.id}.json"
            logging.info(f"-- Saving to file: {file_path}")
            with open(file_path, 'w') as f:
                json.dump(categoryJson, f)
            wait = random.uniform(INTERVAL_MIN_SECONDS, INTERVAL_MAX_SECONDS)
            logging.info(f"Waiting {wait:.1f} seconds...")
            await asyncio.sleep(wait)

            # logging.info(f"--Products in category: {len(categoryDto.hits)}") # TODO: print num products and see if any product requests reaches 1000
    # log we are done at end time and how long it acutally took
    end_time = datetime.utcnow()
    logging.info(f"Done fetching data from Rema. Took {end_time - start_time} (Estimated: {estimated_fetch_duration})")

    # TODO: Convert to domain objects


# Example category: 655370

# Returns a json response with all products in a category
def _fetch_products_json(category_id: int):
    body = {
        "params": "query",
        "hitsPerPage": 1000,
        "facets": ["labels"],
        "facetFilters": [f"category_id:{category_id}"]
    }

    response = requests.post(URL_CATEGORY, json=body)
    response.raise_for_status()
    json: dict = response.json()

    return json

    # Convert json response to dtos
    # category: CategoryDto = category_dto_from_dict(json)

    # return category


def _fetch_departments():

    response = requests.get(URL_DEPARTMENTS)
    response.raise_for_status()

    json: dict = response.json()

    # Convert json response to dtos
    departmentDtos: list[RemaDepartmentDto] = departments_dto_from_json(json)

    return departmentDtos
