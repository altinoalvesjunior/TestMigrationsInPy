import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_setting_charset(self):
        resp = StreamResponse()

        resp.content_type = 'text/html'
        resp.charset = 'koi8-r'
        self.assertEqual('text/html; charset=koi8-r',
                         resp.headers['content-type'])