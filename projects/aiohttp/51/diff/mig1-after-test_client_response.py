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

def test_del(loop):
    response = ClientResponse('get', URL('http://del-cl-resp.org'))
    response._post_init(loop)
    connection = mock.Mock()
    response._setup_connection(connection)
    loop.set_exception_handler(lambda loop, ctx: None)
    with pytest.warns(ResourceWarning):
        del response
        gc.collect()
    connection.close.assert_called_with()