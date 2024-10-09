import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_write_payload_chunked_filter_mutiple_chunks(transport):
    write = transport.write = mock.Mock()
    msg = protocol.Response(transport, 200)
    msg.send_headers()

    msg.add_chunking_filter(2)
    msg.write(b'data1')
    msg.write(b'data2')
    msg.write_eof()
    content = b''.join([c[1][0] for c in list(write.mock_calls)])
    assert content.endswith(
        b'2\r\nda\r\n2\r\nta\r\n2\r\n1d\r\n2\r\nat\r\n'
        b'2\r\na2\r\n0\r\n\r\n')