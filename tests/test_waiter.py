from datetime import timedelta
from unittest.mock import AsyncMock, Mock

import pytest

from src.waiter import Waiter


@pytest.fixture
def mock_random():
    return Mock()


@pytest.fixture
def mock_sleep():
    return AsyncMock()


@pytest.fixture
def valid_min_max_wait() -> tuple[timedelta, timedelta]:
    return timedelta(seconds=1), timedelta(seconds=5)


def test_init__with_valid_params__no_error(
    valid_min_max_wait: tuple[timedelta, timedelta],
    mock_random: Mock,
    mock_sleep: AsyncMock,
):
    min_wait, max_wait = valid_min_max_wait
    waiter = Waiter(min_wait, max_wait, mock_random, mock_sleep)
    assert waiter is not None


@pytest.mark.parametrize(
    "min_wait, max_wait",
    [
        # min_wait is negative
        (timedelta(seconds=-1), timedelta(seconds=5)),
        # max_wait is negative
        (timedelta(seconds=1), timedelta(seconds=-5)),
        # min_wait is greater than max_wait
        (
            timedelta(seconds=5),
            timedelta(seconds=1),
        ),
    ],
)
def test_init__with_invalid_params__raises_exception(
    min_wait: timedelta, max_wait: timedelta, mock_random: Mock, mock_sleep: AsyncMock
):
    with pytest.raises(ValueError):
        Waiter(min_wait, max_wait, mock_random, mock_sleep)


@pytest.mark.asyncio
async def test_wait__is_called_once_with_correct_params(
    mock_random: Mock, mock_sleep: AsyncMock
):
    min_wait_sec = 1
    max_wait_sec = 5
    random_val_generated = 3

    mock_random.return_value = random_val_generated

    waiter = Waiter(
        timedelta(seconds=min_wait_sec),
        timedelta(seconds=max_wait_sec),
        mock_random,
        mock_sleep,
    )
    await waiter.wait()

    mock_random.assert_called_once_with(min_wait_sec, max_wait_sec)
    mock_sleep.assert_called_once_with(random_val_generated)


@pytest.mark.asyncio
async def test_estimate_total_wait__with_valid_params__returns_correct_result(
    mock_random: Mock,
    mock_sleep: AsyncMock,
):
    # ARRANGE
    min_wait_sec = 1
    max_wait_sec = 5
    total_calls = 10
    expected_wait = 30

    # Sut
    waiter = Waiter(
        timedelta(seconds=min_wait_sec),
        timedelta(seconds=max_wait_sec),
        mock_random,
        mock_sleep,
    )

    # ACT
    estimated_wait = waiter.estimate_total_wait(total_calls)

    # ASSERT
    assert estimated_wait.total_seconds() == expected_wait


def test_estimate_total_wait__with_invalid_params__raises_exception(
    valid_min_max_wait: tuple[timedelta, timedelta],
    mock_random: Mock,
    mock_sleep: AsyncMock,
):
    min_wait, max_wait = valid_min_max_wait
    waiter = Waiter(min_wait, max_wait, mock_random, mock_sleep)

    with pytest.raises(ValueError):
        waiter.estimate_total_wait(0)
