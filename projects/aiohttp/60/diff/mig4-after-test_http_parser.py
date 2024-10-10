import aiohttp
import pytest
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload:
    def test_parse_chunked_payload_size_error(self, stream):
        out = aiohttp.FlowControlDataQueue(stream)
        p = HttpPayloadParser(out, chunked=True)
        with pytest.raises(http_exceptions.TransferEncodingError):
            p.feed_data(b'blah\r\n')
        assert isinstance(out.exception(),
                          http_exceptions.TransferEncodingError)