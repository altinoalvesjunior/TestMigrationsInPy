import asyncio
import gc
import pytest
from unittest import mock
from yarl import URL
from aiohttp import StreamReader
from aiohttp.client_reqrep import ClientResponse

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

def test_override_flow_control(loop):
    class MyResponse(ClientResponse):
        flow_control_class = StreamReader
    response = MyResponse('get', URL('http://my-cl-resp.org'))
    response._post_init(loop)
    response._setup_connection(mock.Mock())
    assert isinstance(response.content, StreamReader)
    response.close()