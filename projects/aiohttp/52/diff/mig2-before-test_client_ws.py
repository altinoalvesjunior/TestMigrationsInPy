import asyncio
import base64
import hashlib
import os
import unittest
from unittest import mock

import aiohttp
from aiohttp import errors, hdrs, helpers
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

    @mock.patch('aiohttp.client.os')
    @mock.patch('aiohttp.client.ClientSession.get')
    def test_ws_connect_with_origin(self, m_req, m_os):
        resp = mock.Mock()
        resp.status = 403
        m_os.urandom.return_value = self.key_data
        m_req.return_value = helpers.create_future(self.loop)
        m_req.return_value.set_result(resp)
        origin = 'https://example.org/page.html'
        with self.assertRaises(errors.WSServerHandshakeError):
            self.loop.run_until_complete(
                aiohttp.ws_connect(
                    'http://test.org',
                    loop=self.loop,
                    origin=origin))
        self.assertIn(hdrs.ORIGIN, m_req.call_args[1]["headers"])
        self.assertEqual(m_req.call_args[1]["headers"][hdrs.ORIGIN], origin)