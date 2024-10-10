import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock
import zlib

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    _comp = zlib.compressobj(wbits=-zlib.MAX_WBITS)
    _COMPRESSED = b''.join([_comp.compress(b'data'), _comp.flush()])

    def test_http_payload_parser_deflate(self):
        length = len(self._COMPRESSED)
        out = aiohttp.FlowControlDataQueue(self.stream)
        p = HttpPayloadParser(
            out, length=length, compression='deflate')
        p.feed_data(self._COMPRESSED)
        self.assertEqual(b'data', b''.join(d for d, _ in out._buffer))
        self.assertTrue(out.is_eof())