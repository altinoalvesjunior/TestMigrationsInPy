import unittest
import asyncio
from aiohttp import parsers

class TestStreamParser(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_set_parser_feed_existing_stop(self):
        def LinesParser(out, buf):
            try:
                chunk = yield from buf.readuntil(b'\n')
                out.feed_data(chunk, len(chunk))
                chunk = yield from buf.readuntil(b'\n')
                out.feed_data(chunk, len(chunk))
            finally:
                out.feed_eof()
        stream = parsers.StreamParser(loop=self.loop)
        stream.feed_data(b'line1')
        stream.feed_data(b'\r\nline2\r\ndata')
        s = stream.set_parser(LinesParser)
        self.assertEqual(
            b'line1\r\nline2\r\n', b''.join(d for d, _ in s._buffer))
        self.assertEqual(b'data', bytes(stream._buffer))
        self.assertIsNone(stream._parser)
        self.assertTrue(s._eof)