import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_skip_exc(buf):
    buf.set_exception(ValueError())
    p = buf.skip(3)
    with pytest.raises(ValueError):
        next(p)