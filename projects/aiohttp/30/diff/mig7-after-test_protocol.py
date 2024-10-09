import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_keep_alive(transport):
    msg = protocol.Response(transport, 200, close=True)
    assert not msg.keep_alive()
    msg.keepalive = True
    assert msg.keep_alive()

    msg.force_close()
    assert not msg.keep_alive()