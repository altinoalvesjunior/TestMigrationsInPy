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

def test_tcp_connector_clear_resolved_hosts(loop):
    conn = aiohttp.TCPConnector(loop=loop)
    info = object()
    conn._cached_hosts[('localhost', 123)] = info
    conn._cached_hosts[('localhost', 124)] = info
    conn.clear_resolved_hosts('localhost', 123)
    assert conn.resolved_hosts == {('localhost', 124): info}
    conn.clear_resolved_hosts('localhost', 123)
    assert conn.resolved_hosts == {('localhost', 124): info}
    with pytest.warns(DeprecationWarning):
        conn.clear_resolved_hosts()
    assert conn.resolved_hosts == {}