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

@pytest.mark.xfail
@asyncio.coroutine
def test_del_with_scheduled_cleanup(loop):
    conn = aiohttp.BaseConnector(loop=loop, keepalive_timeout=0.01)
    transp = unittest.mock.Mock()
    conn._conns['a'] = [(transp, 'proto', 123)]
    conns_impl = conn._conns
    conn._start_cleanup_task()
    exc_handler = unittest.mock.Mock()
    loop.set_exception_handler(exc_handler)
    with pytest.warns(ResourceWarning):
        # obviously doesn't deletion because loop has a strong
        # reference to connector's instance method, isn't it?
        del conn
        yield from asyncio.sleep(0.01, loop=loop)
        gc.collect()
    assert not conns_impl
    transp.close.assert_called_with()
    msg = {'connector': unittest.mock.ANY,  # conn was deleted
           'message': 'Unclosed connector'}
    if loop.get_debug():
        msg['source_traceback'] = unittest.mock.ANY
    exc_handler.assert_called_with(loop, msg)