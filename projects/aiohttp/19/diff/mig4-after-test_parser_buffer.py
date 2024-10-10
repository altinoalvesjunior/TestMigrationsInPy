import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_read_exc_multiple(buf):
    p = buf.read(3)
    next(p)
    p.send(b'1')
    exc = ValueError()
    buf.set_exception(exc)
    assert buf.exception() is exc
    p = buf.read(3)
    with pytest.raises(ValueError):
        next(p)