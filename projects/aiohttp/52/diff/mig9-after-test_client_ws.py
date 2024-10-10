import asyncio
import base64
import hashlib
import os
from unittest import mock

import pytest
import aiohttp
from aiohttp import hdrs, helpers
from aiohttp._ws_impl import WS_KEY


@pytest.fixture
def key_data():
    return os.urandom(16)

@pytest.fixture
def key(key_data):
    return base64.b64encode(key_data)

@pytest.fixture
def ws_key(key):
    return base64.b64encode(hashlib.sha1(key + WS_KEY).digest()).decode()

@asyncio.coroutine
def test_close(loop, ws_key, key_data):
    resp = mock.Mock()
    resp.status = 101
    resp.headers = {
        hdrs.UPGRADE: hdrs.WEBSOCKET,
        hdrs.CONNECTION: hdrs.UPGRADE,
        hdrs.SEC_WEBSOCKET_ACCEPT: ws_key,
    }
    with mock.patch('aiohttp.client.WebSocketWriter') as WebSocketWriter:
        with mock.patch('aiohttp.client.os') as m_os:
            with mock.patch('aiohttp.client.ClientSession.get') as m_req:
                m_os.urandom.return_value = key_data
                m_req.return_value = helpers.create_future(loop)
                m_req.return_value.set_result(resp)
                writer = WebSocketWriter.return_value = mock.Mock()
                reader = mock.Mock()
                resp.connection.reader.set_parser.return_value = reader
                resp = yield from aiohttp.ws_connect('http://test.org',
                                                     loop=loop)
                assert not resp.closed
                msg = aiohttp.WSMessage(aiohttp.MsgType.CLOSE, b'', b'')
                reader.read.return_value = helpers.create_future(loop)
                reader.read.return_value.set_result(msg)
                res = yield from resp.close()
                writer.close.assert_called_with(1000, b'')
                assert resp.closed
                assert res
                assert resp.exception() is None
                # idempotent
                res = yield from resp.close()
                assert not res
                assert writer.close.call_count == 1