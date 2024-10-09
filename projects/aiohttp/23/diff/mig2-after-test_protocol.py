import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_start_response(transport):
    msg = protocol.Response(transport, 200, close=True)

    assert msg.transport is transport
    assert msg.status == 200
    assert msg.reason == "OK"
    assert msg.closing
    assert msg.status_line == 'HTTP/1.1 200 OK\r\n'