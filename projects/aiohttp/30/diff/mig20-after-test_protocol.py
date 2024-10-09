import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_default_headers_server(transport):
    msg = protocol.Response(transport, 200)
    msg._add_default_headers()

    assert 'SERVER' in msg.headers