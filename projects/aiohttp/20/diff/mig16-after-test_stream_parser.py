import pytest
from aiohttp import parsers

@pytest.fixture
def lines_parser():
    return parsers.LinesParser()

def test_feed_parser(loop, lines_parser):
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(lines_parser)
    stream.feed_data(b'line1')
    stream.feed_data(b'\r\nline2\r\ndata')
    assert b'data' == bytes(stream._buffer)
    stream.feed_eof()
    assert ([(bytearray(b'line1\r\n'), 7), (bytearray(b'line2\r\n'), 7)] ==
            list(s._buffer))
    assert b'data' == bytes(stream._buffer)
    assert s.is_eof()