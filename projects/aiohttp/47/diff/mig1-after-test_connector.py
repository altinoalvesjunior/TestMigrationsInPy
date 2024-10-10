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

def test_tcp_connector_ctor(loop):
    conn = aiohttp.TCPConnector(loop=loop)
    assert conn.verify_ssl
    assert conn.fingerprint is None
    with pytest.warns(DeprecationWarning):
        assert not conn.resolve
    assert not conn.use_dns_cache
    assert conn.family == 0
    with pytest.warns(DeprecationWarning):
        assert conn.resolved_hosts == {}
    assert conn.resolved_hosts == {}