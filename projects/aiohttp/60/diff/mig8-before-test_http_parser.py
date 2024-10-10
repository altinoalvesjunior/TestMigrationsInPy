import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_http_payload_parser_length_zero(self):
        out = aiohttp.FlowControlDataQueue(self.stream)
        p = HttpPayloadParser(out, length=0)
        self.assertTrue(p.done)
        self.assertTrue(out.is_eof())