import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload:
    def test_parse_eof_payload(self, stream):
        out = aiohttp.FlowControlDataQueue(stream)
        p = HttpPayloadParser(out, readall=True)
        p.feed_data(b'data')
        p.feed_eof()

        assert out.is_eof()
        assert [(bytearray(b'data'), 4)] == list(out._buffer)