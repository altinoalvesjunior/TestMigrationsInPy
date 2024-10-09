import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_add_headers_upgrade_websocket(transport):
    msg = protocol.Response(transport, 200)
    msg.add_headers(('upgrade', 'test'))
    assert [] == list(msg.headers)

    msg.add_headers(('upgrade', 'websocket'))
    assert [('UPGRADE', 'websocket')] == list(msg.headers.items())