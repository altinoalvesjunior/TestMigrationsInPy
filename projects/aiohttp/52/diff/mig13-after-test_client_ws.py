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
def test_send_data_type_errors(ws_key, key_data, loop):
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
                WebSocketWriter.return_value = mock.Mock()
                resp = yield from aiohttp.ws_connect('http://test.org',
                                                     loop=loop)
                pytest.raises(TypeError, resp.send_str, b's')
                pytest.raises(TypeError, resp.send_bytes, 'b')
                pytest.raises(TypeError, resp.send_json, set())