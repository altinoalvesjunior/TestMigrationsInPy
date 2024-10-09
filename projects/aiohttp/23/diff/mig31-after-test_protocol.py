import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_prepare_eof(transport):
    msg = protocol.Response(transport, 200, http_version=(1, 0))
    eof = msg._write_eof_payload = mock.Mock()
    eof.return_value = iter([1, 2, 3])
    msg.send_headers()
    assert eof.called