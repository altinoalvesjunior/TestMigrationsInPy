import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_default_charset(self):
        resp = StreamResponse()

        self.assertIsNone(resp.charset)