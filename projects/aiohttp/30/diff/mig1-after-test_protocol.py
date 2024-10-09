import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_start_request(transport):
    msg = protocol.Request(
        transport, 'GET', '/index.html', close=True)

    assert msg.transport is transport
    assert msg.closing
    assert msg.status_line == 'GET /index.html HTTP/1.1\r\n'