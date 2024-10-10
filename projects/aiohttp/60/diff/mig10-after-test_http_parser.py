import aiohttp
import pytest
from aiohttp.http_parser import DeflateBuffer
from unittest import mock

class TestDeflateBuffer:
    def test_feed_data(self, stream):
        buf = aiohttp.FlowControlDataQueue(stream)
        dbuf = DeflateBuffer(buf, 'deflate')

        dbuf.decompressor = mock.Mock()
        dbuf.decompressor.decompress.return_value = b'line'

        dbuf.feed_data(b'data', 4)
        assert [b'line'] == list(d for d, _ in buf._buffer)