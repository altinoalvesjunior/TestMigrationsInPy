import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_set_parser_feed_existing_exc(self):
        def p(out, buf):
            yield from buf.read(1)
            raise ValueError()
        stream = parsers.StreamParser(loop=self.loop)
        stream.feed_data(b'line1')
        s = stream.set_parser(p)
        self.assertIsInstance(s.exception(), ValueError)