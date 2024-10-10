import asyncio
import gc
import pytest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    yield loop
    loop.close()
    gc.collect()

def test_repr(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    response.status = 200
    response.reason = 'Ok'
    assert '<ClientResponse(http://def-cl-resp.org) [200 Ok]>'\
        in repr(response)