import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_parse_chunked_payload_size_error(self):
        out = aiohttp.FlowControlDataQueue(self.stream)
        p = HttpPayloadParser(out, chunked=True)
        self.assertRaises(
            http_exceptions.TransferEncodingError, p.feed_data, b'blah\r\n')
        self.assertIsInstance(
            out.exception(), http_exceptions.TransferEncodingError)