import pytest
from aiohttp import parsers

def test_unset_parser_eof_unhandled_eof(loop):
    def p(out, buf):
        while True:
            yield  # read chunk
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(p)
    stream.feed_data(b'line1')
    stream.unset_parser()
    assert isinstance(s.exception(), RuntimeError)
    assert not s.is_eof()