import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_default_headers_connection_upgrade(transport):
    msg = protocol.Response(transport, 200)
    msg.upgrade = True
    msg._add_default_headers()

    headers = [r for r in msg.headers.items() if r[0] == 'CONNECTION']
    assert [('CONNECTION', 'upgrade')] == headers