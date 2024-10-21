import unittest
import asyncio
from aiohttp.web import StreamResponse
from aiohttp.protocol import HttpVersion10

class TestStreamResponse(unittest.TestCase):

    def test_chunked_encoding_forbidden_for_http_10(self):
        req = self.make_request('GET', '/', version=HttpVersion10)
        resp = StreamResponse()
        resp.enable_chunked_encoding()

        with self.assertRaisesRegex(
                RuntimeError,
                "Using chunked encoding is forbidden for HTTP/1.0"):
            self.loop.run_until_complete(resp.prepare(req))