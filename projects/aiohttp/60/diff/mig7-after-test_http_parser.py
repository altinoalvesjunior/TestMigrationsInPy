import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock
import zlib

class TestParsePayload:
    def test_http_payload_parser_deflate_no_wbits(self, stream):
        comp = zlib.compressobj()
        COMPRESSED = b''.join([comp.compress(b'data'), comp.flush()])

        length = len(COMPRESSED)
        out = aiohttp.FlowControlDataQueue(stream)
        p = HttpPayloadParser(
            out, length=length, compression='deflate')
        p.feed_data(COMPRESSED)
        assert b'data' == b''.join(d for d, _ in out._buffer)
        assert out.is_eof()