import pytest
from unittest import mock
from aiohttp import protocol

@pytest.fixture
def transport():
    return mock.Mock()

def test_write_drain(transport):
    msg = protocol.Response(transport, 200, http_version=(1, 0))
    msg._send_headers = True

    msg.write(b'1' * (64 * 1024 * 2))
    assert not transport.drain.called

    msg.write(b'1', drain=True)
    assert transport.drain.called
    assert msg._output_size == 0