import aiohttp
import pytest
from aiohttp.http_parser import DeflateBuffer
from unittest import mock

class TestDeflateBuffer:
    def test_empty_body(self, stream):
        buf = aiohttp.FlowControlDataQueue(stream)
        dbuf = DeflateBuffer(buf, 'deflate')
        dbuf.feed_eof()

        assert buf.at_eof()