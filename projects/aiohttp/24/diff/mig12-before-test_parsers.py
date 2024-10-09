import unittest
from aiohttp import parsers, errors

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_readuntil_limit(self):
        buf = self._make_one()
        p = buf.readuntil(b'\n', 4)
        next(p)
        p.send(b'1')
        p.send(b'234')
        self.assertRaises(errors.LineLimitExceededParserError, p.send, b'5')