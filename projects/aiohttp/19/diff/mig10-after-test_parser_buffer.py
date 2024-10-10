import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_skip(buf):
    p = buf.skip(3)
    next(p)
    p.send(b'1')
    try:
        p.send(b'234')
    except StopIteration as exc:
        res = exc.value
    assert res is None
    assert b'4' == bytes(buf)