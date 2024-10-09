import pytest
from unittest import mock
from aiohttp import parsers

@pytest.fixture
def stream():
    return mock.Mock()

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_lines_parser(buf, stream, loop):
    out = parsers.FlowControlDataQueue(stream, loop=loop)
    p = parsers.LinesParser()(out, buf)
    next(p)
    for d in (b'line1', b'\r\n', b'lin', b'e2\r', b'\ndata'):
        p.send(d)
    assert ([(bytearray(b'line1\r\n'), 7), (bytearray(b'line2\r\n'), 7)] ==
            list(out._buffer))
    try:
        p.throw(parsers.EofStream())
    except StopIteration:
        pass
    assert bytes(buf) == b'data'