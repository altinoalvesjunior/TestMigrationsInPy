import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_readuntil_exc(self):
        buf = self._make_one()
        buf.set_exception(ValueError())
        p = buf.readuntil(b'\n', 4)
        self.assertRaises(ValueError, next, p)