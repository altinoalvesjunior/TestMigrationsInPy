import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_content_length(self):
        resp = StreamResponse()
        self.assertIsNone(resp.content_length)