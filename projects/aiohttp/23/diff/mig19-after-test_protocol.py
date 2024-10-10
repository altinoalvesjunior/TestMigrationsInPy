import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_default_headers(transport):
    msg = protocol.Response(transport, 200)
    msg._add_default_headers()

    headers = [r for r, _ in msg.headers.items()]
    assert 'DATE' in headers
    assert 'CONNECTION' in headers