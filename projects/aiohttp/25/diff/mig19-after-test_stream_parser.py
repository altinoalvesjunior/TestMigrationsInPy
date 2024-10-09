import pytest
from aiohttp import parsers

def test_feed_eof_exc(loop):
    def p(out, buf):
        try:
            while True:
                yield  # read chunk
        except parsers.EofStream:
            raise ValueError()
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(p)
    stream.feed_data(b'line1')
    assert s.exception() is None
    stream.feed_eof()
    assert isinstance(s.exception(), ValueError)