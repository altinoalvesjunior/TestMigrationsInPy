import pytest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

def test_resp_host():
    response = ClientResponse('get', URL('http://del-cl-resp.org'))
    with pytest.warns(DeprecationWarning):
        assert 'del-cl-resp.org' == response.host