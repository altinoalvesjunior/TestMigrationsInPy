import asyncio
import gc
import socket
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
def test_tcp_connector_resolve_host_use_dns_cache(loop):
    conn = aiohttp.TCPConnector(loop=loop, use_dns_cache=True)

    res = yield from conn._resolve_host('localhost', 8080)
    assert res
    for rec in res:
        if rec['family'] == socket.AF_INET:
            assert rec['host'] == '127.0.0.1'
            assert rec['hostname'] == 'localhost'
            assert rec['port'] == 8080
        elif rec['family'] == socket.AF_INET6:
            assert rec['host'] == '::1'
            assert rec['hostname'] == 'localhost'
            assert rec['port'] == 8080