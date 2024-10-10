import unittest
from aiohttp.web import StreamResponse

def test_reset_charset(self):
    resp = StreamResponse()
    resp.content_type = 'text/html'
    resp.charset = None
    assert resp.charset is None