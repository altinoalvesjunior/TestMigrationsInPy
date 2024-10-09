import pytest
from unittest import mock
from aiohttp import parsers

@pytest.fixture
def stream():
    return mock.Mock()

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_chunks_parser(stream, loop, buf):
    out = parsers.FlowControlDataQueue(stream, loop=loop)
    p = parsers.ChunksParser(5)(out, buf)
    next(p)
    for d in (b'line1', b'lin', b'e2d', b'ata'):
        p.send(d)
    assert ([(bytearray(b'line1'), 5), (bytearray(b'line2'), 5)] ==
            list(out._buffer))
    try:
        p.throw(parsers.EofStream())
    except StopIteration:
        pass
    assert bytes(buf) == b'data'