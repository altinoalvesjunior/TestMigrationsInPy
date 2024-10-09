import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_add_headers_connection_keepalive(transport):
    msg = protocol.Response(transport, 200)
    msg.add_headers(('connection', 'keep-alive'))
    assert [] == list(msg.headers)
    assert msg.keepalive
    msg.add_headers(('connection', 'close'))
    assert not msg.keepalive