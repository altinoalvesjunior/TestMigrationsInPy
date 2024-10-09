import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_add_headers_upgrade(transport):
    msg = protocol.Response(transport, 200)
    assert not msg.upgrade
    msg.add_headers(('connection', 'upgrade'))
    assert msg.upgrade