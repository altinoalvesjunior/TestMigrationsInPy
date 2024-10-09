import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_force_close(transport):
    msg = protocol.Response(transport, 200)
    assert not msg.closing
    msg.force_close()
    assert msg.closing