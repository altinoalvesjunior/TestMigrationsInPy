import asyncio
import gc
import pytest
import aiohttp
from aiohttp import helpers, ClientRequest

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

@asyncio.coroutine
def test_connect_timeout(loop):
    conn = aiohttp.BaseConnector(loop=loop)
    conn._create_connection = unittest.mock.Mock()
    conn._create_connection.return_value = helpers.create_future(loop)
    conn._create_connection.return_value.set_exception(
        asyncio.TimeoutError())

    with pytest.raises(aiohttp.ClientTimeoutError):
        req = unittest.mock.Mock()
        yield from conn.connect(req)