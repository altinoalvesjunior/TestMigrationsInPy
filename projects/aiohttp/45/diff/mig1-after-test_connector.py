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

def test_del(loop):
    conn = aiohttp.BaseConnector(loop=loop)
    transp = unittest.mock.Mock()
    conn._conns['a'] = [(transp, 'proto', 123)]
    conns_impl = conn._conns
    exc_handler = unittest.mock.Mock()
    loop.set_exception_handler(exc_handler)
    with pytest.warns(ResourceWarning):
        del conn
        gc.collect()
    assert not conns_impl
    transp.close.assert_called_with()
    msg = {'connector': unittest.mock.ANY,  # conn was deleted
           'connections': unittest.mock.ANY,
           'message': 'Unclosed connector'}
    if loop.get_debug():
        msg['source_traceback'] = unittest.mock.ANY
    exc_handler.assert_called_with(loop, msg)