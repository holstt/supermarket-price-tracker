from datetime import timedelta
from unittest.mock import AsyncMock, Mock, create_autospec

import pytest

from src.rema.client import RemaClient
from src.rema.scraper import RemaScraper
from src.storage import DataStorage
from src.utils import get_utc_now
from src.waiter import Waiter
from tests.dto_builders import DepartmentCategoryDtoBuilder, DepartmentDtoBuilder


@pytest.mark.asyncio
async def test_data_storage_called_with_correct_args():
    # ARRANGE

    # Data
    test_category = DepartmentCategoryDtoBuilder().with_id(1).build()
    test_department = (
        DepartmentDtoBuilder().with_id(1).with_categories([test_category]).build()
    )
    test_data_to_save = {"some": "data"}

    # Mocks
    mock_client: RemaClient = create_autospec(spec=RemaClient)
    mock_client.fetch_departments = Mock(return_value=[test_department])
    mock_client.fetch_products_json = Mock(return_value=test_data_to_save)

    mock_storage: DataStorage = create_autospec(spec=DataStorage)
    mock_storage.save_data = Mock()

    waiter: Waiter = create_autospec(Waiter)
    waiter.estimate_total_wait = Mock(return_value=(timedelta(seconds=1)))

    get_current_time = lambda: get_utc_now()

    # Sut
    scraper = RemaScraper(mock_storage, mock_client, waiter, get_current_time)

    # ACT
    await scraper.scrape()

    # ASSERT
    expected_file_name = f"dep_{test_department.id}_cat_{test_category.id}.json"
    mock_storage.save_data.assert_called_with(expected_file_name, {"some": "data"})
