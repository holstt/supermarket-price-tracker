import logging

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


class RemaClient:
    URL_DEPARTMENTS = "https://cphapp.rema1000.dk/api/v1/catalog/store/1/departments-v2"
    URL_CATEGORY = "https://flwdn2189e-dsn.algolia.net/1/indexes/aws-prod-products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.21.1&x-algolia-application-id=FLWDN2189E&x-algolia-api-key=fa20981a63df668e871a87a8fbd0caed"

    def fetch_departments(self):
        response = requests.get(self.URL_DEPARTMENTS)
        response.raise_for_status()
        json = response.json()

        # Convert json response to dtos
        departmentDtos: list[RemaDepartmentDto] = departments_dto_from_json(json)
        return departmentDtos

    # Example category: 655370
    # Returns a json response with all products in a category
    def fetch_products_json(self, category_id: int):
        body = {
            "params": "query",
            "hitsPerPage": 1000,
            "facets": ["labels"],
            "facetFilters": [f"category_id:{category_id}"],
        }

        response = requests.post(self.URL_CATEGORY, json=body)
        response.raise_for_status()
        json = response.json()

        return json

        # TODO: Convert json response to dtos
        # category: CategoryDto = category_dto_from_dict(json)

        # return category
