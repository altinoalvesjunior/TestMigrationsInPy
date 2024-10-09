import pytest
from aiohttp import parsers

def test_feed_none_data(loop):
    stream = parsers.StreamParser(loop=loop)
    stream.feed_data(None)
    assert b'' == bytes(stream._buffer)