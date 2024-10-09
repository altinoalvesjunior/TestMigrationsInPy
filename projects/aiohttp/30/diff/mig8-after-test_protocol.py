import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_keep_alive_http10(transport):
    msg = protocol.Response(transport, 200, http_version=(1, 0))
    assert not msg.keepalive
    assert not msg.keep_alive()

    msg = protocol.Response(transport, 200, http_version=(1, 1))
    assert msg.keepalive is None