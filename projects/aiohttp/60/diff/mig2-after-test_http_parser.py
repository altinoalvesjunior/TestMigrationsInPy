import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload:
    def test_parse_no_body(self, stream):
        out = aiohttp.FlowControlDataQueue(stream)
        p = HttpPayloadParser(out, method='PUT')

        assert out.is_eof()
        assert p.done