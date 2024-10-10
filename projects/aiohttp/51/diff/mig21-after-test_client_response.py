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

def test_get_encoding_unknown(loop):
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response._post_init(loop)
    response.headers = {'Content-Type': 'application/json'}
    with mock.patch('aiohttp.client_reqrep.chardet') as m_chardet:
        m_chardet.detect.return_value = {'encoding': None}
        assert response._get_encoding() == 'utf-8'