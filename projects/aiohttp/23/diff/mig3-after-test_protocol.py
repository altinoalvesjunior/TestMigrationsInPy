import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_start_response_with_reason(transport):
    msg = protocol.Response(transport, 333, close=True,
                            reason="My Reason")

    assert msg.status == 333
    assert msg.reason == "My Reason"
    assert msg.status_line == 'HTTP/1.1 333 My Reason\r\n'