import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_start_response_with_unknown_reason(transport):
    msg = protocol.Response(transport, 777, close=True)

    assert msg.status == 777
    assert msg.reason == "777"
    assert msg.status_line == 'HTTP/1.1 777 777\r\n'