import unittest
import aiohttp
from aiohttp.http_parser import DeflateBuffer
from unittest import mock

class TestDeflateBuffer(unittest.TestCase):

    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_feed_data(self):
        buf = aiohttp.FlowControlDataQueue(self.stream)
        dbuf = DeflateBuffer(buf, 'deflate')

        dbuf.decompressor = mock.Mock()
        dbuf.decompressor.decompress.return_value = b'line'

        dbuf.feed_data(b'data', 4)
        self.assertEqual([b'line'], list(d for d, _ in buf._buffer))