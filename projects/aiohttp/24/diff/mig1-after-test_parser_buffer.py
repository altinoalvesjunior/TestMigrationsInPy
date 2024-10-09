import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_feed_data(buf):
    buf.feed_data(b'')
    assert len(buf) == 0
    buf.feed_data(b'data')
    assert len(buf) == 4
    assert bytes(buf) == b'data'