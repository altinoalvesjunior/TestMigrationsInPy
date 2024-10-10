import gc
import pytest
from unittest import mock
from aiohttp.connector import Connection

def test_detach(connector, key, request, transport, protocol, loop):
    conn = Connection(connector, key, request,
                      transport, protocol, loop)
    assert not conn.closed
    conn.detach()
    assert conn._transport is None
    assert not connector._release.called
    assert conn.closed