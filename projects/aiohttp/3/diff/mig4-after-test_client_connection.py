import gc
import pytest
from unittest import mock
from aiohttp.connector import Connection

def test_release(connector, key, request, transport, protocol, loop):
    conn = Connection(connector, key, request,
                      transport, protocol, loop)
    assert not conn.closed
    conn.release()
    assert not transport.close.called
    assert conn._transport is None
    connector._release.assert_called_with(
        key, request, transport, protocol,
        should_close=False)
    assert conn.closed