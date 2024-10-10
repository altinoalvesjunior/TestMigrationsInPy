import unittest
from aiohttp.web import StreamResponse

def test_default_charset(self):
    resp = StreamResponse()
    assert resp.charset is None