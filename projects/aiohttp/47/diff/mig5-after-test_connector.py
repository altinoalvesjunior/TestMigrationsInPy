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

def test_tcp_connector_clear_dns_cache(loop):
    conn = aiohttp.TCPConnector(loop=loop)
    info = object()
    conn._cached_hosts[('localhost', 123)] = info
    conn._cached_hosts[('localhost', 124)] = info
    conn.clear_dns_cache('localhost', 123)
    assert conn.cached_hosts == {('localhost', 124): info}
    conn.clear_dns_cache('localhost', 123)
    assert conn.cached_hosts == {('localhost', 124): info}
    conn.clear_dns_cache()
    assert conn.cached_hosts == {}