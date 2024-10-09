import pytest
from aiohttp import parsers

def test_feed_eof_stop(loop):
    def p(out, buf):
        try:
            while True:
                yield  # read chunk
        except parsers.EofStream:
            out.feed_eof()
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(p)
    stream.feed_data(b'line1')
    stream.feed_eof()
    assert s._eof