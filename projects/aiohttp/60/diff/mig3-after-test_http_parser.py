import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload:
    def test_parse_length_payload_eof(self, stream):
        out = aiohttp.FlowControlDataQueue(stream)

        p = HttpPayloadParser(out, length=4)
        p.feed_data(b'da')

        with pytest.raises(http_exceptions.ContentLengthError):
            p.feed_eof()