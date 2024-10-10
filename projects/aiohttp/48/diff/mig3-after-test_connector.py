import asyncio
import gc
import ssl
import pytest
import aiohttp

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

def test_respect_precreated_ssl_context(loop):
    ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    conn = aiohttp.TCPConnector(loop=loop, ssl_context=ctx)
    assert ctx is conn.ssl_context