import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_write_payload_eof(transport):
    write = transport.write = mock.Mock()
    msg = protocol.Response(transport, 200, http_version=(1, 0))
    msg.send_headers()

    msg.write(b'data1')
    assert msg.headers_sent

    msg.write(b'data2')
    msg.write_eof()

    content = b''.join([c[1][0] for c in list(write.mock_calls)])
    assert b'data1data2' == content.split(b'\r\n\r\n', 1)[-1]