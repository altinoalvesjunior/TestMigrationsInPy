import asyncio
import gc
import pytest
import aiohttp
from aiohttp import helpers, ClientRequest

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

@asyncio.coroutine
def test_connect_oserr(loop):
    conn = aiohttp.BaseConnector(loop=loop)
    conn._create_connection = unittest.mock.Mock()
    conn._create_connection.return_value = helpers.create_future(loop)
    err = OSError(1, 'permission error')
    conn._create_connection.return_value.set_exception(err)
    with pytest.raises(aiohttp.ClientOSError) as ctx:
        req = unittest.mock.Mock()
        yield from conn.connect(req)
    assert 1 == ctx.value.errno
    assert ctx.value.strerror.startswith('Cannot connect to')
    assert ctx.value.strerror.endswith('[permission error]')