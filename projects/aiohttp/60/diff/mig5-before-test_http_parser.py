import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_http_payload_parser_length(self):
        out = aiohttp.FlowControlDataQueue(self.stream)
        p = HttpPayloadParser(out, length=2)
        eof, tail = p.feed_data(b'1245')
        self.assertTrue(eof)

        self.assertEqual(b'12', b''.join(d for d, _ in out._buffer))
        self.assertEqual(b'45', tail)