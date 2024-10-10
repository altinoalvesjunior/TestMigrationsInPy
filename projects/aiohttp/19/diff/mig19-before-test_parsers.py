import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_lines_parser(self):
        out = parsers.FlowControlDataQueue(self.stream, loop=self.loop)
        buf = self._make_one()
        p = parsers.LinesParser()(out, buf)
        next(p)
        for d in (b'line1', b'\r\n', b'lin', b'e2\r', b'\ndata'):
            p.send(d)
        self.assertEqual(
            [(bytearray(b'line1\r\n'), 7), (bytearray(b'line2\r\n'), 7)],
            list(out._buffer))
        try:
            p.throw(parsers.EofStream())
        except StopIteration:
            pass
        self.assertEqual(bytes(buf), b'data')