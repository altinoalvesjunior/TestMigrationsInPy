import pytest
from unittest import mock
from aiohttp import hdrs, protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_add_headers_hop_headers(transport):
    msg = protocol.Response(transport, 200)
    msg.HOP_HEADERS = (hdrs.TRANSFER_ENCODING,)

    msg.add_headers(('connection', 'test'), ('transfer-encoding', 't'))
    assert [] == list(msg.headers)