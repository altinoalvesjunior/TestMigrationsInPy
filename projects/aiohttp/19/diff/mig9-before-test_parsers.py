import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_wait_exc(self):
        buf = self._make_one()
        buf.set_exception(ValueError())
        p = buf.wait(3)
        self.assertRaises(ValueError, next, p)