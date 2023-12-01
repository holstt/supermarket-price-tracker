# Abstract class scraper
from abc import ABC, abstractmethod

from src.storage import DataStorage


class Scraper(ABC):
    # DataStorage: Where to save the scraped data
    def __init__(self, data_storage: DataStorage):
        self._data_storage = data_storage

    # X: Avoid storage by returning a generator?
    @abstractmethod
    async def scrape(self):
        pass
