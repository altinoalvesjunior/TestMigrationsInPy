import unittest
import asyncio
from unittest import mock
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):

    @mock.patch('aiohttp.web_reqrep.ResponseImpl')
    def test_chunk_size(self, ResponseImpl):
        req = self.make_request('GET', '/')
        resp = StreamResponse()
        self.assertFalse(resp.chunked)

        resp.enable_chunked_encoding(chunk_size=8192)
        self.assertTrue(resp.chunked)

        msg = self.loop.run_until_complete(resp.prepare(req))
        self.assertTrue(msg.chunked)
        msg.add_chunking_filter.assert_called_with(8192)
        self.assertIsNotNone(msg.filter)