import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_setting_content_type(self):
        resp = StreamResponse()

        resp.content_type = 'text/html'
        self.assertEqual('text/html', resp.headers['content-type'])