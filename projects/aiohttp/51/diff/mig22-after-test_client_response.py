import pytest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

def test_raise_for_status_2xx():
    response = ClientResponse('get', URL('http://def-cl-resp.org'))
    response.status = 200
    response.reason = 'OK'
    response.raise_for_status()  # should not raise