import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_add_headers_length(transport):
    msg = protocol.Response(transport, 200)
    assert msg.length is None

    msg.add_headers(('content-length', '42'))
    assert 42 == msg.length