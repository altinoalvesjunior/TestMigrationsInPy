import pytest
from aiohttp import parsers

def test_set_parser_feed_existing_eof_unhandled_eof(loop):
    def p(out, buf):
        while True:
            yield  # read chunk
    stream = parsers.StreamParser(loop=loop)
    stream.feed_data(b'line1')
    stream.feed_eof()
    s = stream.set_parser(p)
    assert not s.is_eof()
    assert isinstance(s.exception(), RuntimeError)