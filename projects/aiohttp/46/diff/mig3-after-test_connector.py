import asyncio
import gc
import pytest
import aiohttp
from aiohttp import helpers, Connection, ClientRequest

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

@asyncio.coroutine
def test_connect(loop):
    tr, proto = unittest.mock.Mock(), unittest.mock.Mock()
    proto.is_connected.return_value = True

    req = ClientRequest('GET', 'http://host:80',
                        loop=loop,
                        response_class=unittest.mock.Mock())

    conn = aiohttp.BaseConnector(loop=loop)
    key = ('host', 80, False)
    conn._conns[key] = [(tr, proto, loop.time())]
    conn._create_connection = unittest.mock.Mock()
    conn._create_connection.return_value = helpers.create_future(loop)
    conn._create_connection.return_value.set_result((tr, proto))
    connection = yield from conn.connect(req)
    assert not conn._create_connection.called
    assert connection._transport is tr
    assert connection._protocol is proto
    assert isinstance(connection, Connection)
    connection.close()