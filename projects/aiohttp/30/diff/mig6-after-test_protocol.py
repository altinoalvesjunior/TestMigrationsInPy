import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_force_chunked(transport):
    msg = protocol.Response(transport, 200)
    assert not msg.chunked
    msg.enable_chunked_encoding()
    assert msg.chunked