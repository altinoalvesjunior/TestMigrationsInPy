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

def test_wait_for_100_1(loop):
    response = ClientResponse(
        'get', URL('http://python.org'), continue100=object())
    response._post_init(loop)
    assert response.waiting_for_continue()
    response.close()