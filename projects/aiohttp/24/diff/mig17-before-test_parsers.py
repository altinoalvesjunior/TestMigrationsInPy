import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_skipuntil(self):
        buf = self._make_one()
        p = buf.skipuntil(b'\n')
        next(p)
        p.send(b'123')
        try:
            p.send(b'\n456\n')
        except StopIteration:
            pass
        self.assertEqual(b'456\n', bytes(buf))
        p = buf.skipuntil(b'\n')
        try:
            next(p)
        except StopIteration:
            pass
        self.assertEqual(b'', bytes(buf))