import pytest
from aiohttp.multidict import CIMultiDict
from aiohttp.web import Response

def test_response_ctor():
    resp = Response()
    assert 200 == resp.status
    assert 'OK' == resp.reason
    assert resp.body is None
    assert 0 == resp.content_length
    assert CIMultiDict([('CONTENT-LENGTH', '0')]) == resp.headers