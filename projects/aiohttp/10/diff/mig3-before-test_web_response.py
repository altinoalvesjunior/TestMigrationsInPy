import unittest
from aiohttp.web import StreamResponse

def test_content_length_setter(self):
    resp = StreamResponse()

    resp.content_length = 234
    assert 234 == resp.content_length