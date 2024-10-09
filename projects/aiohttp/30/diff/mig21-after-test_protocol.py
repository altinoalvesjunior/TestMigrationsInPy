import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_default_headers_chunked(transport):
    msg = protocol.Response(transport, 200)
    msg._add_default_headers()

    headers = [r for r, _ in msg.headers.items()]
    assert 'TRANSFER-ENCODING' not in headers

    msg = protocol.Response(transport, 200)
    msg.enable_chunked_encoding()
    msg.send_headers()

    headers = [r for r, _ in msg.headers.items()]
    assert 'TRANSFER-ENCODING' in headers