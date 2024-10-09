import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_add_header_non_ascii(transport):
    msg = protocol.Response(transport, 200)
    assert [] == list(msg.headers)

    with pytest.raises(AssertionError):
        msg.add_header('тип-контента', 'текст/плейн')