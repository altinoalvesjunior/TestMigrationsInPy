import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_feed_data(self):
        buf = self._make_one()
        buf.feed_data(b'')
        self.assertEqual(len(buf), 0)
        buf.feed_data(b'data')
        self.assertEqual(len(buf), 4)
        self.assertEqual(bytes(buf), b'data')