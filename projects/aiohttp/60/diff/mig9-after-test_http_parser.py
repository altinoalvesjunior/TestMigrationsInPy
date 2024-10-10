import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock
import brotli

class TestParsePayload:
    @pytest.mark.skipif(brotli is None, reason="brotli is not installed")
    def test_http_payload_brotli(self, stream):
        compressed = brotli.compress(b'brotli data')
        out = aiohttp.FlowControlDataQueue(stream)
        p = HttpPayloadParser(
            out, length=len(compressed), compression='br')
        p.feed_data(compressed)
        assert b'brotli data' == b''.join(d for d, _ in out._buffer)
        assert out.is_eof()