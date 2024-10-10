import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_parse_eof_payload(self):
        out = aiohttp.FlowControlDataQueue(self.stream)
        p = HttpPayloadParser(out, readall=True)
        p.feed_data(b'data')
        p.feed_eof()

        self.assertTrue(out.is_eof())
        self.assertEqual([(bytearray(b'data'), 4)], list(out._buffer))