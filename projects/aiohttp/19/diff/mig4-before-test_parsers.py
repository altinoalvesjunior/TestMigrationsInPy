import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_read_exc_multiple(self):
        buf = self._make_one()
        p = buf.read(3)
        next(p)
        p.send(b'1')
        exc = ValueError()
        buf.set_exception(exc)
        self.assertIs(buf.exception(), exc)
        p = buf.read(3)
        self.assertRaises(ValueError, next, p)