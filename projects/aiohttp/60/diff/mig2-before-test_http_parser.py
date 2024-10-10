import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_parse_no_body(self):
        out = aiohttp.FlowControlDataQueue(self.stream)
        p = HttpPayloadParser(out, method='PUT')

        self.assertTrue(out.is_eof())
        self.assertTrue(p.done)