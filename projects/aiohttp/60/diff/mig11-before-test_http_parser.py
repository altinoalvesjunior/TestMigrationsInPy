import unittest
import aiohttp
from aiohttp.http_parser import DeflateBuffer
from unittest import mock

class TestDeflateBuffer(unittest.TestCase):

    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_feed_data_err(self):
        buf = aiohttp.FlowControlDataQueue(self.stream)
        dbuf = DeflateBuffer(buf, 'deflate')

        exc = ValueError()
        dbuf.decompressor = mock.Mock()
        dbuf.decompressor.decompress.side_effect = exc

        self.assertRaises(
            http_exceptions.ContentEncodingError, dbuf.feed_data, b'data', 4)