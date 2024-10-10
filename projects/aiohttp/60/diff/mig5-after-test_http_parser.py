import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload:
    def test_http_payload_parser_length(self, stream):
        out = aiohttp.FlowControlDataQueue(stream)
        p = HttpPayloadParser(out, length=2)
        eof, tail = p.feed_data(b'1245')
        assert eof

        assert b'12' == b''.join(d for d, _ in out._buffer)
        assert b'45' == tail