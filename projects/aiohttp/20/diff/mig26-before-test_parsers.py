import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_eof_exc(self):
        def p(out, buf):
            while True:
                yield  # read chunk
        class CustomEofErr(Exception):
            pass
        stream = parsers.StreamParser(
            eof_exc_class=CustomEofErr, loop=self.loop)
        s = stream.set_parser(p)
        stream.feed_eof()
        self.assertIsInstance(s.exception(), CustomEofErr)