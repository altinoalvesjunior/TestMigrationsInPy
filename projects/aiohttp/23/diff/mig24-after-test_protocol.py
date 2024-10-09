import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_default_headers_connection_keep_alive(transport):
    msg = protocol.Response(transport, 200)
    msg.keepalive = True
    msg._add_default_headers()

    headers = [r for r in msg.headers.items() if r[0] == 'CONNECTION']
    assert [('CONNECTION', 'keep-alive')] == headers