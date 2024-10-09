import gc
import pytest
from unittest import mock
from aiohttp.connector import Connection

@pytest.fixture
def key():
    return object()
@pytest.fixture
def connector():
    return mock.Mock()
@pytest.fixture
def request():
    return mock.Mock()
@pytest.fixture
def transport():
    return mock.Mock()
@pytest.fixture
def protocol():
    return mock.Mock()