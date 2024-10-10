import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_drop_content_length_header_on_setting_len_to_None(self):
        resp = StreamResponse()

        resp.content_length = 1
        self.assertEqual("1", resp.headers['Content-Length'])
        resp.content_length = None
        self.assertNotIn('Content-Length', resp.headers)