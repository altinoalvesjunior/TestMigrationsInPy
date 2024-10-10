import asyncio
import gc
import pytest
from unittest import mock
from yarl import URL
from aiohttp import helpers
from aiohttp.client_reqrep import ClientResponse

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

@asyncio.coroutine
def test_read_and_release_connection(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    def side_effect(*args, **kwargs):
        fut = helpers.create_future(loop)
        fut.set_result(b'payload')
        return fut
    content = response.content = mock.Mock()
    content.read.side_effect = side_effect
    res = yield from response.read()
    assert res == b'payload'
    assert response._connection is None