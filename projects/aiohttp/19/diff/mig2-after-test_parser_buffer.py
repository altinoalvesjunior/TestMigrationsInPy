import pytest
from aiohttp import parsers

@pytest.fixture
def buf():
    return parsers.ParserBuffer()

def test_feed_data_after_exception(buf):
    buf.feed_data(b'data')
    exc = ValueError()
    buf.set_exception(exc)
    buf.feed_data(b'more')
    assert len(buf) == 4
    assert bytes(buf) == b'data'