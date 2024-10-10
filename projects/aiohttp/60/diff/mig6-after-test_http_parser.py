import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock
import zlib

class TestParsePayload:
    _comp = zlib.compressobj(wbits=-zlib.MAX_WBITS)
    _COMPRESSED = b''.join([_comp.compress(b'data'), _comp.flush()])

    def test_http_payload_parser_deflate(self, stream):
        length = len(self._COMPRESSED)
        out = aiohttp.FlowControlDataQueue(stream)
        p = HttpPayloadParser(
            out, length=length, compression='deflate')
        p.feed_data(self._COMPRESSED)
        assert b'data' == b''.join(d for d, _ in out._buffer)
        assert out.is_eof()