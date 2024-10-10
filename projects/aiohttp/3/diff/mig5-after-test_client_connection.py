import gc
import pytest
from unittest import mock
from aiohttp.connector import Connection

def test_release_released(connector, key, request, transport, protocol, loop):
    conn = Connection(connector, key, request,
                      transport, protocol, loop)
    conn.release()
    connector._release.reset_mock()
    conn.release()
    assert not transport.close.called
    assert conn._transport is None
    assert not connector._release.called