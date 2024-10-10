import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_last_modified_reset(self):
        resp = StreamResponse()

        resp.last_modified = 0
        resp.last_modified = None
        self.assertEqual(resp.last_modified, None)