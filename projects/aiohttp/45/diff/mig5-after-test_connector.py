import asyncio
import gc
import pytest
import aiohttp

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

@asyncio.coroutine
def test_create_conn(loop):
    conn = aiohttp.BaseConnector(loop=loop)
    with pytest.raises(NotImplementedError):
        yield from conn._create_connection(object())