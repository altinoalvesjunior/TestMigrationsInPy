import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_prepare_length(transport):
    msg = protocol.Response(transport, 200)
    w_l_p = msg._write_length_payload = mock.Mock()
    w_l_p.return_value = iter([1, 2, 3])

    msg.add_headers(('content-length', '42'))
    msg.send_headers()

    assert w_l_p.called
    assert (42,) == w_l_p.call_args[0]