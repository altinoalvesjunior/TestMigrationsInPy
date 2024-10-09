import pytest
from aiohttp import parsers

DATA = b'line1\nline2\nline3\n'

def test_feed_data(loop):
    stream = parsers.StreamParser(loop=loop)
    stream.feed_data(DATA)
    assert DATA == bytes(stream._buffer)