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
def test_connect_with_limit(loop):
    tr, proto = unittest.mock.Mock(), unittest.mock.Mock()
    proto.is_connected.return_value = True

    req = ClientRequest('GET', 'http://host:80',
                        loop=loop,
                        response_class=unittest.mock.Mock())

    conn = aiohttp.BaseConnector(loop=loop, limit=1)
    key = ('host', 80, False)
    conn._conns[key] = [(tr, proto, loop.time())]
    conn._create_connection = unittest.mock.Mock()
    conn._create_connection.return_value = helpers.create_future(loop)
    conn._create_connection.return_value.set_result((tr, proto))

    connection1 = yield from conn.connect(req)
    assert connection1._transport == tr

    assert 1 == len(conn._acquired[key])

    acquired = False

    @asyncio.coroutine
    def f():
        nonlocal acquired
        connection2 = yield from conn.connect(req)
        acquired = True
        assert 1 == len(conn._acquired[key])
        connection2.release()
    task = helpers.ensure_future(f(), loop=loop)
    yield from asyncio.sleep(0.01, loop=loop)
    assert not acquired
    connection1.release()
    yield from asyncio.sleep(0, loop=loop)
    assert acquired
    yield from task
    conn.close()