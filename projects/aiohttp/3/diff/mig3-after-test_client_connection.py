import gc
import pytest
from unittest import mock
from aiohttp.connector import Connection

def test_close(connector, key, request, transport, protocol, loop):
    conn = Connection(connector, key, request,
                      transport, protocol, loop)
    assert not conn.closed
    conn.close()
    assert conn._transport is None
    connector._release.assert_called_with(
        key, request, transport, protocol,
        should_close=True)
    assert conn.closed
