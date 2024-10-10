import pytest
from aiohttp import parsers

@pytest.fixture
def lines_parser():
    return parsers.LinesParser()

def test_set_parser_feed_existing(loop, lines_parser):
    stream = parsers.StreamParser(loop=loop)
    stream.feed_data(b'line1')
    stream.feed_data(b'\r\nline2\r\ndata')
    s = stream.set_parser(lines_parser)
    assert ([(bytearray(b'line1\r\n'), 7), (bytearray(b'line2\r\n'), 7)] ==
            list(s._buffer))
    assert b'data' == bytes(stream._buffer)
    assert stream._parser is not None
    stream.unset_parser()
    assert stream._parser is None
    assert b'data' == bytes(stream._buffer)
    assert s._eof