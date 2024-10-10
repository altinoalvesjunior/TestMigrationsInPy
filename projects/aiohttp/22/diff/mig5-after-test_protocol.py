import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_write_payload_deflate_and_chunked(transport):
    write = transport.write = mock.Mock()
    msg = protocol.Response(transport, 200)
    msg.send_headers()
    msg.add_compression_filter('deflate')
    msg.add_chunking_filter(2)
    msg.write(b'data')
    msg.write_eof()
    chunks = [c[1][0] for c in list(write.mock_calls)]
    assert all(chunks)
    content = b''.join(chunks)
    assert (b'2\r\nKI\r\n2\r\n,I\r\n2\r\n\x04\x00\r\n0\r\n\r\n' ==
            content.split(b'\r\n\r\n', 1)[-1])