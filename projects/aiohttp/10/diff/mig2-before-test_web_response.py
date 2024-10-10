import unittest
from aiohttp.web import StreamResponse

def test_content_length(self):
    resp = StreamResponse()
    assert resp.content_length is None