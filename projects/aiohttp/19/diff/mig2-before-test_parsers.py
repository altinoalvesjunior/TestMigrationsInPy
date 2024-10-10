import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_feed_data_after_exception(self):
        buf = self._make_one()
        buf.feed_data(b'data')
        exc = ValueError()
        buf.set_exception(exc)
        buf.feed_data(b'more')
        self.assertEqual(len(buf), 4)
        self.assertEqual(bytes(buf), b'data')