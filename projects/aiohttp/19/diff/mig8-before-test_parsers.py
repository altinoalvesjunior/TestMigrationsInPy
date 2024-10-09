import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_wait(self):
        buf = self._make_one()
        p = buf.wait(3)
        next(p)
        p.send(b'1')
        try:
            p.send(b'234')
        except StopIteration as exc:
            res = exc.value
        self.assertEqual(res, b'123')
        self.assertEqual(b'1234', bytes(buf))