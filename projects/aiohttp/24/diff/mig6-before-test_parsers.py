import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_readsome(self):
        buf = self._make_one()
        p = buf.readsome(3)
        next(p)
        try:
            p.send(b'1')
        except StopIteration as exc:
            res = exc.value
        self.assertEqual(res, b'1')
        p = buf.readsome(2)
        next(p)
        try:
            p.send(b'234')
        except StopIteration as exc:
            res = exc.value
        self.assertEqual(res, b'23')
        self.assertEqual(b'4', bytes(buf))