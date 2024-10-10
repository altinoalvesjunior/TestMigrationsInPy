import asyncio
import gc
import pytest
from unittest import mock
import aiohttp

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

def test_del_with_closed_loop(loop):
    conn = aiohttp.BaseConnector(loop=loop)
    transp = unittest.mock.Mock()
    conn._conns['a'] = [(transp, 'proto', 123)]
    conns_impl = conn._conns
    conn._start_cleanup_task()
    exc_handler = unittest.mock.Mock()
    loop.set_exception_handler(exc_handler)
    loop.close()
    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()
    assert not conns_impl
    assert not transp.close.called
    assert exc_handler.called