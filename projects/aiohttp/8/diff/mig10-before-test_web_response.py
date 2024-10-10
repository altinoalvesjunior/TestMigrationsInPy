import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_reset_charset_after_setting(self):
        resp = StreamResponse()

        resp.content_type = 'text/html'
        resp.charset = 'koi8-r'
        resp.charset = None
        self.assertIsNone(resp.charset)