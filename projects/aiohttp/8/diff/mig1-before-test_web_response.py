import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_ctor(self):
        resp = StreamResponse()
        self.assertEqual(200, resp.status)
        self.assertIsNone(resp.keep_alive)