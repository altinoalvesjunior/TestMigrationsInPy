import unittest
import asyncio
from unittest import mock
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):

    @mock.patch('aiohttp.web_reqrep.ResponseImpl')
    def test_compression_no_accept(self, ResponseImpl):
        req = self.make_request('GET', '/')
        resp = StreamResponse()
        self.assertFalse(resp.chunked)

        self.assertFalse(resp.compression)
        resp.enable_compression()
        self.assertTrue(resp.compression)

        msg = self.loop.run_until_complete(resp.prepare(req))
        self.assertFalse(msg.add_compression_filter.called)