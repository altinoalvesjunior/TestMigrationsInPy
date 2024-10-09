import pytest
from aiohttp import parsers

def test_feed_parser_exc(loop):
    def p(out, buf):
        yield  # read chunk
        raise ValueError()
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(p)
    stream.feed_data(b'line1')
    assert isinstance(s.exception(), ValueError)
    assert b'' == bytes(stream._buffer)