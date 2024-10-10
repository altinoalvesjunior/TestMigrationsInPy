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

@asyncio.coroutine
def test_json_no_content(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    response.headers = {
        'Content-Type': 'data/octet-stream'}
    response._content = b''
    with mock.patch('aiohttp.client_reqrep.client_logger') as m_log:
        res = yield from response.json()
    assert res is None
    m_log.warning.assert_called_with(
        'Attempt to decode JSON with unexpected mimetype: %s',
        'data/octet-stream')