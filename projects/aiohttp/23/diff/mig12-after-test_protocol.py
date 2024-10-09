import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_add_header_invalid_value_type(transport):
    msg = protocol.Response(transport, 200)
    assert [] == list(msg.headers)

    with pytest.raises(AssertionError):
        msg.add_header('content-type', {'test': 'plain'})

    with pytest.raises(AssertionError):
        msg.add_header(list('content-type'), 'text/plain')