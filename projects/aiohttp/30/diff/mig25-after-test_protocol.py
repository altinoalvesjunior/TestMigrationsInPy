import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_send_headers(transport):
    write = transport.write = mock.Mock()

    msg = protocol.Response(transport, 200)
    msg.add_headers(('content-type', 'plain/html'))
    assert not msg.is_headers_sent()

    msg.send_headers()

    content = b''.join([arg[1][0] for arg in list(write.mock_calls)])

    assert content.startswith(b'HTTP/1.1 200 OK\r\n')
    assert b'CONTENT-TYPE: plain/html' in content
    assert msg.headers_sent
    assert msg.is_headers_sent()
    # cleanup
    msg.writer.close()