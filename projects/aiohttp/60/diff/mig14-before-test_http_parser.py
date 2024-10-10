import unittest
import aiohttp
from aiohttp.http_parser import DeflateBuffer
from unittest import mock

class TestDeflateBuffer(unittest.TestCase):

    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_empty_body(self):
        buf = aiohttp.FlowControlDataQueue(self.stream)
        dbuf = DeflateBuffer(buf, 'deflate')
        dbuf.feed_eof()

        self.assertTrue(buf.at_eof())