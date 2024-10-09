import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_send_headers_nomore_add(transport):
    msg = protocol.Response(transport, 200)
    msg.add_headers(('content-type', 'plain/html'))
    msg.send_headers()

    with pytest.raises(AssertionError):
        msg.add_header('content-type', 'plain/html')
    # cleanup
    msg.writer.close()