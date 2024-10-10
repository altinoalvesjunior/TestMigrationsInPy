import pytest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

def test_repr_non_ascii_reason():
    response = ClientResponse('get', URL('http://fake-host.org/path'))
    response.reason = '\u03bb'
    assert "<ClientResponse(http://fake-host.org/path) [None \\u03bb]>"\
        in repr(response)