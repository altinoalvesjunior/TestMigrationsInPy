import unittest
import aiohttp
from aiohttp.http_parser import HttpPayloadParser
from unittest import mock
import pytest
import brotli

class TestParsePayload(unittest.TestCase):
    def setUp(self):
        self.stream = mock.Mock()
        asyncio.set_event_loop(None)

    @pytest.mark.skipif(brotli is None, reason="brotli is not installed")
    def test_http_payload_brotli(self):
        compressed = brotli.compress(b'brotli data')
        out = aiohttp.FlowControlDataQueue(self.stream)
        p = HttpPayloadParser(
            out, length=len(compressed), compression='br')
        p.feed_data(compressed)
        self.assertEqual(b'brotli data', b''.join(d for d, _ in out._buffer))
        self.assertTrue(out.is_eof())