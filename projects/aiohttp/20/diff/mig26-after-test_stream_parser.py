import pytest
from aiohttp import parsers

def test_eof_exc(loop):
    def p(out, buf):
        while True:
            yield  # read chunk
    class CustomEofErr(Exception):
        pass
    stream = parsers.StreamParser(eof_exc_class=CustomEofErr, loop=loop)
    s = stream.set_parser(p)
    stream.feed_eof()
    assert isinstance(s.exception(), CustomEofErr)