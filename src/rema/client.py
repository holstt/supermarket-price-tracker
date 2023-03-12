import logging
from pathlib import Path
from time import sleep
import requests
from src.rema.category_dto import CategoryDto, category_dto_from_dict
from src.rema.department_dtos import DepartmentCategoryDto, RemaDepartmentDto, rema_dto_from_dict
import json

URL_DEPARTMENTS = "https://cphapp.rema1000.dk/api/v1/catalog/store/1/departments-v2"

# Api key is Rema not ours
URL_CATEGORY = "https://flwdn2189e-dsn.algolia.net/1/indexes/aws-prod-products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.21.1&x-algolia-application-id=FLWDN2189E&x-algolia-api-key=fa20981a63df668e871a87a8fbd0caed"


def get_rema_data():
    logging.info("Fetching data from Rema...")
    logging.info("Fetching all departments...")
    departmentDtos = fetch_departments()
    # iterate over departments and categories, then fetch products in each category
    for department in departmentDtos:
        logging.info(f"Department {department.id}: {department.name}...")
        for category in department.categories:
            logging.info(f"-Category {category.id}: {category.name}...")
            logging.info(f"Fetching products in category...")
            categoryJson: dict = fetch_products_json(category.id)
            logging.info(f"Saving products to file...")
            with open(f'data/category_{category.id}.json', 'w') as f:
                json.dump(categoryJson, f)
            sleep(2)
            # print(f"--Products in category: {len(categoryDto.hits)}")

    # TODO: Convert to domain objects


# Example category: 655370


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
    departmentDtos: list[RemaDepartmentDto] = rema_dto_from_dict(json)

    return departmentDtos
