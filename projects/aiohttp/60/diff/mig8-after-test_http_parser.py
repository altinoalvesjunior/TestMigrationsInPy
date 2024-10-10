import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload:
    def test_http_payload_parser_length_zero(self, stream):
        out = aiohttp.FlowControlDataQueue(stream)
        p = HttpPayloadParser(out, length=0)
        assert p.done
        assert out.is_eof()