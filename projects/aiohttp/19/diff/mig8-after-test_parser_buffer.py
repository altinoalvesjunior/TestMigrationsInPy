import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_wait(buf):
    p = buf.wait(3)
    next(p)
    p.send(b'1')
    try:
        p.send(b'234')
    except StopIteration as exc:
        res = exc.value
    assert res == b'123'
    assert b'1234' == bytes(buf)