import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_unset_parser_stop(self):
        def p(out, buf):
            try:
                while True:
                    yield  # read chunk
            except parsers.EofStream:
                out.feed_eof()
        stream = parsers.StreamParser(loop=self.loop)
        s = stream.set_parser(p)
        stream.feed_data(b'line1')
        stream.unset_parser()
        self.assertTrue(s._eof)