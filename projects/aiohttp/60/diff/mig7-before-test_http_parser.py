import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock
import zlib

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    def test_http_payload_parser_deflate_no_wbits(self):
        comp = zlib.compressobj()
        COMPRESSED = b''.join([comp.compress(b'data'), comp.flush()])

        length = len(COMPRESSED)
        out = aiohttp.FlowControlDataQueue(self.stream)
        p = HttpPayloadParser(
            out, length=length, compression='deflate')
        p.feed_data(COMPRESSED)
        self.assertEqual(b'data', b''.join(d for d, _ in out._buffer))
        self.assertTrue(out.is_eof())