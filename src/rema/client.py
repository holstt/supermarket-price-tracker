import logging
from pathlib import Path
import random
from time import sleep
import requests
from src.rema.json_dtos.category_dto import CategoryDto, category_dto_from_dict
from src.rema.json_dtos.department_dto import DepartmentCategoryDto, RemaDepartmentDto, departments_dto_from_json
import json

# Rema API reverse engineered from their website shop:
# - Department URL returns all departments each with a list of category ids
# - Category URL returns all products in a specific category given a category id
# As such we need to fetch all departments to get the category ids, then fetch all products in each category

URL_DEPARTMENTS = "https://cphapp.rema1000.dk/api/v1/catalog/store/1/departments-v2"
# Api key is Rema not ours
URL_CATEGORY = "https://flwdn2189e-dsn.algolia.net/1/indexes/aws-prod-products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.21.1&x-algolia-application-id=FLWDN2189E&x-algolia-api-key=fa20981a63df668e871a87a8fbd0caed"


def save_rema_data():
    logging.info("Fetching data from Rema...")
    logging.info("Fetching all departments...")
    departmentDtos = fetch_departments()
    logging.info(
        f"Found {len(departmentDtos)} departments and {sum(len(department.categories) for department in departmentDtos)} categories")

    random.shuffle(departmentDtos)

    # iterate over departments and categories, then fetch products in each category
    for department in departmentDtos:
        logging.info(
            f"For department {department.id}: {department.name} ({departmentDtos.index(department) + 1}/{len(departmentDtos)})")
        for category in department.categories:
            logging.info(
                f"- Fetching category {category.id}: {category.name} ({department.categories.index(category) + 1}/{len(department.categories)})")
            categoryJson: dict = fetch_products_json(category.id)
            file_path = Path(f'data/category_{category.id}.json')
            logging.info(f"-- Saving to file: {file_path}")
            with open(file_path, 'w') as f:
                json.dump(categoryJson, f)
            sleep(random.randint(1, 5))

            # logging.info(f"--Products in category: {len(categoryDto.hits)}")

    # TODO: Convert to domain objects


# Example category: 655370

# Returns a json response with all products in a category
def fetch_products_json(category_id: int):
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


def fetch_departments():

    response = requests.get(URL_DEPARTMENTS)
    response.raise_for_status()

    json: dict = response.json()

    # Convert json response to dtos
    departmentDtos: list[RemaDepartmentDto] = departments_dto_from_json(json)

    return departmentDtos
