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
def test_tcp_connector_resolve_host_twice_use_dns_cache(loop):
    conn = aiohttp.TCPConnector(loop=loop, use_dns_cache=True)

    res = yield from conn._resolve_host('localhost', 8080)
    res2 = yield from conn._resolve_host('localhost', 8080)

    assert res is res2