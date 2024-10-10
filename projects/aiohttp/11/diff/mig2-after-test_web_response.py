import pytest
from aiohttp.multidict import CIMultiDict
from aiohttp.web import Response

def test_ctor_with_headers_and_status():
    resp = Response(body=b'body', status=201, headers={'Age': '12'})
    assert 201 == resp.status
    assert b'body' == resp.body
    assert 4 == resp.content_length
    assert (CIMultiDict([('AGE', '12'), ('CONTENT-LENGTH', '4')]) ==
            resp.headers)