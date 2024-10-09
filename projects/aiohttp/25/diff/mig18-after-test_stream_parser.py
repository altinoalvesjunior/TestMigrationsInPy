import pytest
from aiohttp import parsers

def test_feed_parser_stop(loop):
    def p(out, buf):
        yield  # chunk
    stream = parsers.StreamParser(loop=loop)
    stream.set_parser(p)
    stream.feed_data(b'line1')
    assert stream._parser is None
    assert b'' == bytes(stream._buffer)