import pytest
from aiohttp import parsers, errors

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_waituntil_limit(buf):
    p = buf.waituntil(b'\n', 4)
    next(p)
    p.send(b'1')
    p.send(b'234')
    with pytest.raises(errors.LineLimitExceededParserError):
        p.send(b'5')