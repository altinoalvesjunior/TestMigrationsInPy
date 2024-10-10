import aiohttp
import pytest
from aiohttp.http_parser import DeflateBuffer
from unittest import mock

class TestDeflateBuffer:
    def test_feed_eof_err(self, stream):
        buf = aiohttp.FlowControlDataQueue(stream)
        dbuf = DeflateBuffer(buf, 'deflate')

        dbuf.decompressor = mock.Mock()
        dbuf.decompressor.flush.return_value = b'line'
        dbuf.decompressor.eof = False

        with pytest.raises(http_exceptions.ContentEncodingError):
            dbuf.feed_eof()