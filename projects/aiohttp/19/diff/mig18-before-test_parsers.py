import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_skipuntil_exc(self):
        buf = self._make_one()
        buf.set_exception(ValueError())
        p = buf.skipuntil(b'\n')
        self.assertRaises(ValueError, next, p)