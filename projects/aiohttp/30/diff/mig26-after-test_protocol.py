import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_send_headers_non_ascii(transport):
    write = transport.write = mock.Mock()

    msg = protocol.Response(transport, 200)
    msg.add_headers(('x-header', 'текст'))
    assert not msg.is_headers_sent()

    msg.send_headers()

    content = b''.join([arg[1][0] for arg in list(write.mock_calls)])

    assert content.startswith(b'HTTP/1.1 200 OK\r\n')
    assert b'X-HEADER: \xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82' in content
    assert msg.headers_sent
    assert msg.is_headers_sent()
    # cleanup
    msg.writer.close()