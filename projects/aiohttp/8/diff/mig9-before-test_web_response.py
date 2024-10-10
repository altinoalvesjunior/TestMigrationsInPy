import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_reset_charset(self):
        resp = StreamResponse()

        resp.content_type = 'text/html'
        resp.charset = None
        self.assertIsNone(resp.charset)