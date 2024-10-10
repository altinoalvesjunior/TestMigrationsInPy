import pytest
from aiohttp import parsers

@pytest.fixture
def lines_parser():
    return parsers.LinesParser()

def test_feed_parser2(loop, lines_parser):
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(lines_parser)
    stream.feed_data(b'line1\r\nline2\r\n')
    stream.feed_eof()
    assert ([(bytearray(b'line1\r\n'), 7), (bytearray(b'line2\r\n'), 7)] ==
            list(s._buffer))
    assert b'' == bytes(stream._buffer)
    assert s._eof