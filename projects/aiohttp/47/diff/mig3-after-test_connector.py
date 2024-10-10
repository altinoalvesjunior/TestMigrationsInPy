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

def test_tcp_connector_fingerprint_invalid(loop):
    invalid = b'\x00'
    with pytest.raises(ValueError):
        aiohttp.TCPConnector(loop=loop, fingerprint=invalid)