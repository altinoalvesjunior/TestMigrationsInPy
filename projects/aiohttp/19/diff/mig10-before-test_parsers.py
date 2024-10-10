import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_skip(self):
        buf = self._make_one()
        p = buf.skip(3)
        next(p)
        p.send(b'1')
        try:
            p.send(b'234')
        except StopIteration as exc:
            res = exc.value
        self.assertIsNone(res)
        self.assertEqual(b'4', bytes(buf))