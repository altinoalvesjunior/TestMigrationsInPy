import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_content_length_setter(self):
        resp = StreamResponse()

        resp.content_length = 234
        self.assertEqual(234, resp.content_length)