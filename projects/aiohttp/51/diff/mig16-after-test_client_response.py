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

@asyncio.coroutine
def test_json_custom_loader(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    response.headers = {
        'Content-Type': 'application/json;charset=cp1251'}
    response._content = b'data'
    def custom(content):
        return content + '-custom'
    res = yield from response.json(loads=custom)
    assert res == 'data-custom'