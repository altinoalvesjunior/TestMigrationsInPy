import unittest
import datetime
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def test_last_modified_timestamp(self):
        resp = StreamResponse()

        dt = datetime.datetime(1970, 1, 1, 0, 0, 0, 0, datetime.timezone.utc)

        resp.last_modified = 0
        self.assertEqual(resp.last_modified, dt)

        resp.last_modified = 0.0
        self.assertEqual(resp.last_modified, dt)