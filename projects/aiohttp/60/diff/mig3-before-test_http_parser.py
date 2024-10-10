import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock
import pytest

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_parse_length_payload_eof(self):
        out = aiohttp.FlowControlDataQueue(self.stream)

        p = HttpPayloadParser(out, length=4)
        p.feed_data(b'da')

        with pytest.raises(http_exceptions.ContentLengthError):
            p.feed_eof()