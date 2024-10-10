import pytest
from aiohttp.multidict import CIMultiDict
from aiohttp.web import Response

def test_ctor_content_type():
    resp = Response(content_type='application/json')
    assert 200 == resp.status
    assert 'OK' == resp.reason
    assert (CIMultiDict([('CONTENT-TYPE', 'application/json'),
                         ('CONTENT-LENGTH', '0')]) ==
            resp.headers)