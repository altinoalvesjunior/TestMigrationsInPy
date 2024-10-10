import pytest
from aiohttp import parsers

@pytest.fixture
def lines_parser():
    return parsers.LinesParser()

def test_set_parser_unset(loop, lines_parser):
    stream = parsers.StreamParser(loop=loop)
    s = stream.set_parser(lines_parser)
    stream.feed_data(b'line1\r\nline2\r\n')
    assert ([(bytearray(b'line1\r\n'), 7), (bytearray(b'line2\r\n'), 7)] ==
            list(s._buffer))
    assert b'' == bytes(stream._buffer)
    stream.unset_parser()
    assert s._eof
    assert b'' == bytes(stream._buffer)