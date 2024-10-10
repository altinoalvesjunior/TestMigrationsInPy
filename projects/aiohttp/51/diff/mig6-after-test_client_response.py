import pytest
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

def test_repr_non_ascii_url():
    response = ClientResponse('get', URL('http://fake-host.org/\u03bb'))
    assert "<ClientResponse(http://fake-host.org/%CE%BB) [None None]>"\
        in repr(response)