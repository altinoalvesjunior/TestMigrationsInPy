import unittest
from aiohttp.web import StreamResponse

def test_ctor(self):
    resp = StreamResponse()
    assert 200 == resp.status
    assert resp.keep_alive is None