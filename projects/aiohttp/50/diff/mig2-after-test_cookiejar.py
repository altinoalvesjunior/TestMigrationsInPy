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

def test_dont_recreate_ssl_context(loop):
    conn = aiohttp.TCPConnector(loop=loop)
    ctx = conn.ssl_context
    assert ctx is conn.ssl_context