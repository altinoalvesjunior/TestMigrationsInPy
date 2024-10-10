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
def test_read_and_release_connection_with_error(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    content = response.content = mock.Mock()
    content.read.return_value = helpers.create_future(loop)
    content.read.return_value.set_exception(ValueError)
    with pytest.raises(ValueError):
        yield from response.read()
    assert response._closedimport asyncio
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
def test_read_and_release_connection_with_error(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    content = response.content = mock.Mock()
    content.read.return_value = helpers.create_future(loop)
    content.read.return_value.set_exception(ValueError)
    with pytest.raises(ValueError):
        yield from response.read()
    assert response._closed