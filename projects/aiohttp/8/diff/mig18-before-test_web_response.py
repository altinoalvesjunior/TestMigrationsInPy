import unittest
import asyncio
from unittest import mock
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):

    @mock.patch('aiohttp.web_reqrep.ResponseImpl')
    def test_chunked_encoding(self, ResponseImpl):
        req = self.make_request('GET', '/')
        resp = StreamResponse()
        self.assertFalse(resp.chunked)

        resp.enable_chunked_encoding()
        self.assertTrue(resp.chunked)

        msg = self.loop.run_until_complete(resp.prepare(req))
        self.assertTrue(msg.chunked)