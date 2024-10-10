import aiohttp
import pytest
from aiohttp.http_parser import DeflateBuffer
from unittest import mock

class TestDeflateBuffer:
    def test_feed_data_err(self, stream):
        buf = aiohttp.FlowControlDataQueue(stream)
        dbuf = DeflateBuffer(buf, 'deflate')

        exc = ValueError()
        dbuf.decompressor = mock.Mock()
        dbuf.decompressor.decompress.side_effect = exc

        with pytest.raises(http_exceptions.ContentEncodingError):
            dbuf.feed_data(b'data', 4)