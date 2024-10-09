import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_write_auto_send_headers(transport):
    msg = protocol.Response(transport, 200, http_version=(1, 0))
    msg._send_headers = True

    msg.write(b'data1')
    assert msg.headers_sent
    # cleanup
    msg.writer.close()