import asyncio
import base64
import hashlib
import os
import unittest
from unittest import mock

import aiohttp
from aiohttp import hdrs, helpers
from aiohttp._ws_impl import WS_KEY


class TestWebSocketClient(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.key_data = os.urandom(16)
        self.key = base64.b64encode(self.key_data)
        self.ws_key = base64.b64encode(
            hashlib.sha1(self.key + WS_KEY).digest()).decode()

    def tearDown(self):
        self.loop.close()

    @mock.patch('aiohttp.client.WebSocketWriter')
    @mock.patch('aiohttp.client.os')
    @mock.patch('aiohttp.client.ClientSession.get')
    def test_send_data_after_close(self, m_req, m_os, WebSocketWriter):
        resp = mock.Mock()
        resp.status = 101
        resp.headers = {
            hdrs.UPGRADE: hdrs.WEBSOCKET,
            hdrs.CONNECTION: hdrs.UPGRADE,
            hdrs.SEC_WEBSOCKET_ACCEPT: self.ws_key,
        }
        m_os.urandom.return_value = self.key_data
        m_req.return_value = helpers.create_future(self.loop)
        m_req.return_value.set_result(resp)
        WebSocketWriter.return_value = mock.Mock()
        resp = self.loop.run_until_complete(
            aiohttp.ws_connect(
                'http://test.org', loop=self.loop))
        resp._closed = True
        self.assertRaises(RuntimeError, resp.ping)
        self.assertRaises(RuntimeError, resp.pong)
        self.assertRaises(RuntimeError, resp.send_str, 's')
        self.assertRaises(RuntimeError, resp.send_bytes, b'b')
        self.assertRaises(RuntimeError, resp.send_json, {})