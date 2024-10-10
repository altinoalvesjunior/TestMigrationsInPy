import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_feed_parser_stop(self):
        def p(out, buf):
            yield  # chunk
        stream = parsers.StreamParser(loop=self.loop)
        stream.set_parser(p)
        stream.feed_data(b'line1')
        self.assertIsNone(stream._parser)
        self.assertEqual(b'', bytes(stream._buffer))