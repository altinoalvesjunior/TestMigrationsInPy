import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_skipuntil_exc(buf):
    buf.set_exception(ValueError())
    p = buf.skipuntil(b'\n')
    with pytest.raises(ValueError):
        next(p)