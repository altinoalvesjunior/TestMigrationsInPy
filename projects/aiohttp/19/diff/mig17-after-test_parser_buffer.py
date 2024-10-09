import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_skipuntil(buf):
    p = buf.skipuntil(b'\n')
    next(p)
    p.send(b'123')
    try:
        p.send(b'\n456\n')
    except StopIteration:
        pass
    assert b'456\n' == bytes(buf)
    p = buf.skipuntil(b'\n')
    try:
        next(p)
    except StopIteration:
        pass
    assert b'' == bytes(buf)