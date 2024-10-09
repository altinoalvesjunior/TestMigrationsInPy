import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_readsome_exc(buf):
    buf.set_exception(ValueError())
    p = buf.readsome(3)
    with pytest.raises(ValueError):
        next(p)