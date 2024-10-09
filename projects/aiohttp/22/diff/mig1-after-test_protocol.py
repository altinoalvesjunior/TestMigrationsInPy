import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_write_payload_chunked_filter(transport):
    write = transport.write = mock.Mock()

    msg = protocol.Response(transport, 200)
    msg.send_headers()

    msg.add_chunking_filter(2)
    msg.write(b'data')
    msg.write_eof()

    content = b''.join([c[1][0] for c in list(write.mock_calls)])
    assert content.endswith(b'2\r\nda\r\n2\r\nta\r\n0\r\n\r\n')