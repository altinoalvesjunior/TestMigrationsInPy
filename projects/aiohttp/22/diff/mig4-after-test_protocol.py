import pytest
from unittest import mock
import zlib
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

compressor = zlib.compressobj(wbits=-zlib.MAX_WBITS)
COMPRESSED = b''.join([compressor.compress(b'data'), compressor.flush()])

def test_write_payload_deflate_filter(transport):
    write = transport.write = mock.Mock()
    msg = protocol.Response(transport, 200)
    msg.add_headers(('content-length', '{}'.format(len(COMPRESSED))))
    msg.send_headers()

    msg.add_compression_filter('deflate')
    msg.write(b'data')
    msg.write_eof()

    chunks = [c[1][0] for c in list(write.mock_calls)]
    assert all(chunks)
    content = b''.join(chunks)
    assert COMPRESSED == content.split(b'\r\n\r\n', 1)[-1]