import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_dont_override_response_headers_with_default_values(transport):
    msg = protocol.Response(transport, 200, http_version=(1, 0))
    msg.add_header('DATE', 'now')
    msg.add_header('SERVER', 'custom')
    msg._add_default_headers()
    assert 'custom' == msg.headers['SERVER']
    assert 'now' == msg.headers['DATE']