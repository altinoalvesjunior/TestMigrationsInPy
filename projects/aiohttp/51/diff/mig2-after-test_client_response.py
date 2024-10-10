import asyncio
import gc
import pytest
from unittest import mock
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

def test_close(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    response._connection = mock.Mock()
    response.close()
    assert response.connection is None
    response.close()
    response.close()