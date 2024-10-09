import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_feed_eof_unhandled_eof(self):
        def p(out, buf):
            while True:
                yield  # read chunk
        stream = parsers.StreamParser(loop=self.loop)
        s = stream.set_parser(p)
        stream.feed_data(b'line1')
        stream.feed_eof()
        self.assertFalse(s.is_eof())
        self.assertIsInstance(s.exception(), RuntimeError)