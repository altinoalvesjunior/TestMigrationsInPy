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

def test_close_cancels_cleanup_handle(loop):
    conn = aiohttp.BaseConnector(loop=loop)
    conn._start_cleanup_task()

    assert conn._cleanup_handle is not None
    conn.close()
    assert conn._cleanup_handle is None