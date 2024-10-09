import unittest
from aiohttp import parsers

class TestParserBuffer(unittest.TestCase):
    def _make_one(self):
        return parsers.ParserBuffer()

    def test_chunks_parser(self):
        out = parsers.FlowControlDataQueue(self.stream, loop=self.loop)
        buf = self._make_one()
        p = parsers.ChunksParser(5)(out, buf)
        next(p)
        for d in (b'line1', b'lin', b'e2d', b'ata'):
            p.send(d)
        self.assertEqual(
            [(bytearray(b'line1'), 5), (bytearray(b'line2'), 5)],
            list(out._buffer))
        try:
            p.throw(parsers.EofStream())
        except StopIteration:
            pass
        self.assertEqual(bytes(buf), b'data')