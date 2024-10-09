import unittest
from aiohttp import parsers, errors

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_waituntil_limit(self):
        buf = self._make_one()
        p = buf.waituntil(b'\n', 4)
        next(p)
        p.send(b'1')
        p.send(b'234')
        self.assertRaises(errors.LineLimitExceededParserError, p.send, b'5')
        try:
            p.send(b'\n456')
        except StopIteration as exc:
            res = exc.value
        self.assertEqual(res, b'123\n')
        self.assertEqual(b'123\n456', bytes(buf))