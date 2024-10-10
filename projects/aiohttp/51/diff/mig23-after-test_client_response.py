import pytest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse
import aiohttp

def test_raise_for_status_4xx():
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response.status = 409
    response.reason = 'CONFLICT'
    with pytest.raises(aiohttp.HttpProcessingError) as cm:
        response.raise_for_status()
    assert str(cm.value.code) == '409'
    assert str(cm.value.message) == "CONFLICT"