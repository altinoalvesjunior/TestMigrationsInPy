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

def test_ambigous_verify_ssl_and_ssl_context(loop):
    with pytest.raises(ValueError):
        aiohttp.TCPConnector(
            verify_ssl=False,
            ssl_context=ssl.SSLContext(ssl.PROTOCOL_SSLv23),
            loop=loop)