import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_dont_override_request_headers_with_default_values(transport):
    msg = protocol.Request(
        transport, 'GET', '/index.html', close=True)
    msg.add_header('USER-AGENT', 'custom')
    msg._add_default_headers()
    assert 'custom' == msg.headers['USER-AGENT']