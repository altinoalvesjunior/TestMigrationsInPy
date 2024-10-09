import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_wait_exc(buf):
    buf.set_exception(ValueError())
    p = buf.wait(3)
    with pytest.raises(ValueError):
        next(p)