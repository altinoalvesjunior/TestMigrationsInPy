import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_prepare_chunked_force(transport):
    msg = protocol.Response(transport, 200)
    msg.enable_chunked_encoding()
    chunked = msg._write_chunked_payload = mock.Mock()
    chunked.return_value = iter([1, 2, 3])
    msg.add_headers(('content-length', '42'))
    msg.send_headers()
    assert chunked.called