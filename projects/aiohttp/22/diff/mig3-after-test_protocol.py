import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_write_payload_chunked_large_chunk(transport):
    write = transport.write = mock.Mock()
    msg = protocol.Response(transport, 200)
    msg.send_headers()

    msg.add_chunking_filter(1024)
    msg.write(b'data')
    msg.write_eof()
    content = b''.join([c[1][0] for c in list(write.mock_calls)])
    assert content.endswith(b'4\r\ndata\r\n0\r\n\r\n')