import unittest
import aiohttp
from aiohttp.http_parser import DeflateBuffer
from unittest import mock

class TestDeflateBuffer(unittest.TestCase):

    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_feed_eof_err(self):
        buf = aiohttp.FlowControlDataQueue(self.stream)
        dbuf = DeflateBuffer(buf, 'deflate')

        dbuf.decompressor = mock.Mock()
        dbuf.decompressor.flush.return_value = b'line'
        dbuf.decompressor.eof = False

        self.assertRaises(http_exceptions.ContentEncodingError, dbuf.feed_eof)