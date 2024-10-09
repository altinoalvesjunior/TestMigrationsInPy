import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_readsome(buf):
    p = buf.readsome(3)
    next(p)
    try:
        p.send(b'1')
    except StopIteration as exc:
        res = exc.value
    assert res == b'1'
    p = buf.readsome(2)
    next(p)
    try:
        p.send(b'234')
    except StopIteration as exc:
        res = exc.value
    assert res == b'23'
    assert b'4' == bytes(buf)