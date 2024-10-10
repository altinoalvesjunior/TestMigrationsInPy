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

def test_close_twice(loop):
    tr = unittest.mock.Mock()

    conn = aiohttp.BaseConnector(loop=loop)
    conn._conns[1] = [(tr, object(), object())]
    conn.close()

    assert not conn._conns
    assert tr.close.called
    assert conn.closed

    conn._conns = 'Invalid'  # fill with garbage
    conn.close()
    assert conn.closed