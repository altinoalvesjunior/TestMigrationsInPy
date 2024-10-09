import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_readuntil(self):
        buf = self._make_one()
        p = buf.readuntil(b'\n', 4)
        next(p)
        p.send(b'123')
        try:
            p.send(b'\n456')
        except StopIteration as exc:
            res = exc.value
        self.assertEqual(res, b'123\n')
        self.assertEqual(b'456', bytes(buf))