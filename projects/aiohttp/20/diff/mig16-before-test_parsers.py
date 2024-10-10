import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_feed_parser(self):
        stream = parsers.StreamParser(loop=self.loop)
        lines_parser = parsers.LinesParser()
        s = stream.set_parser(lines_parser)
        stream.feed_data(b'line1')
        stream.feed_data(b'\r\nline2\r\ndata')
        self.assertEqual(b'data', bytes(stream._buffer))
        stream.feed_eof()
        self.assertEqual(
            [(bytearray(b'line1\r\n'), 7), (bytearray(b'line2\r\n'), 7)],
            list(s._buffer))
        self.assertEqual(b'data', bytes(stream._buffer))
        self.assertTrue(s.is_eof())