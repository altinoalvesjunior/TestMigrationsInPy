import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_set_content_length_to_None_on_non_set(self):
        resp = StreamResponse()

        resp.content_length = None
        self.assertNotIn('Content-Length', resp.headers)
        resp.content_length = None
        self.assertNotIn('Content-Length', resp.headers)