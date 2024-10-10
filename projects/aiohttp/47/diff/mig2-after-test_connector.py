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

def test_tcp_connector_ctor_fingerprint_valid(loop):
    valid = b'\xa2\x06G\xad\xaa\xf5\xd8\\J\x99^by;\x06='
    conn = aiohttp.TCPConnector(loop=loop, fingerprint=valid)
    assert conn.fingerprint == valid