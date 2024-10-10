import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_charset_without_content_type(self):
        resp = StreamResponse()

        with self.assertRaises(RuntimeError):
            resp.charset = 'koi8-r'