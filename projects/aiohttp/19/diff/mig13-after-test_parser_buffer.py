import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_readuntil(buf):
    p = buf.readuntil(b'\n', 4)
    next(p)
    p.send(b'123')
    try:
        p.send(b'\n456')
    except StopIteration as exc:
        res = exc.value
    assert res == b'123\n'
    assert b'456' == bytes(buf)