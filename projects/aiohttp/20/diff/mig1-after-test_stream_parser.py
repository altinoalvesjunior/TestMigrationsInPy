import pytest
from aiohttp import parsers

def test_at_eof(loop):
    proto = parsers.StreamParser(loop=loop)
    assert not proto.at_eof()
    proto.feed_eof()
    assert proto.at_eof()