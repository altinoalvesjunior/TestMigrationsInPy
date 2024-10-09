import pytest
from aiohttp import parsers

def test_feed_eof_unhandled_eof(loop):
    def p(out, buf):
        while True:
            yield  # read chunk
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(p)
    stream.feed_data(b'line1')
    stream.feed_eof()
    assert not s.is_eof()
    assert isinstance(s.exception(), RuntimeError)