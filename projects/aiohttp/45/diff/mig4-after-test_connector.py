import asyncio
import gc
import pytest
from unittest import mock
import aiohttp

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

def test_del_empty_conector(loop):
    conn = aiohttp.BaseConnector(loop=loop)
    exc_handler = unittest.mock.Mock()
    loop.set_exception_handler(exc_handler)
    del conn
    assert not exc_handler.called