import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_add_header(transport):
    msg = protocol.Response(transport, 200)
    assert [] == list(msg.headers)

    msg.add_header('content-type', 'plain/html')
    assert [('CONTENT-TYPE', 'plain/html')] == list(msg.headers.items())