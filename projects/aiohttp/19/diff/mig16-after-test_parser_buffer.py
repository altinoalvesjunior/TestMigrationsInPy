import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_waituntil_exc(buf):
    buf.set_exception(ValueError())
    p = buf.waituntil(b'\n', 4)
    with pytest.raises(ValueError):
        next(p)