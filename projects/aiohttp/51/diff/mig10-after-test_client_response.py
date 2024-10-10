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
def test_release(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    fut = helpers.create_future(loop)
    fut.set_result(b'')
    content = response.content = mock.Mock()
    content.readany.return_value = fut
    yield from response.release()
    assert response._connection is None