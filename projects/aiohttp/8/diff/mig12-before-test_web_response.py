import unittest
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_last_modified_initial(self):
        resp = StreamResponse()
        self.assertIsNone(resp.last_modified)