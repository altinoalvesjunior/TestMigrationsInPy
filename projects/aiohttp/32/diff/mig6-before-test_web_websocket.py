import asyncio
import unittest
from unittest import mock
from aiohttp import helpers, MsgType, errors
from aiohttp.web import WebSocketResponse, Request
from aiohttp.protocol import RawRequestMessage, HttpVersion11
from aiohttp import signals

class TestWebWebSocket(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def make_request(self, method, path, headers=None, protocols=False):
        self.app = mock.Mock()
        self.app._debug = False
        if headers is None:
            headers = {'HOST': 'server.example.com',
                       'UPGRADE': 'websocket',
                       'CONNECTION': 'Upgrade',
                       'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==',
                       'ORIGIN': 'http://example.com',
                       'SEC-WEBSOCKET-VERSION': '13'}
            if protocols:
                headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'

        message = RawRequestMessage(method, path, HttpVersion11, headers,
                                    [(k.encode('utf-8'), v.encode('utf-8'))
                                     for k, v in headers.items()],
                                    False, False)
        self.payload = mock.Mock()
        self.transport = mock.Mock()
        self.reader = mock.Mock()
        self.writer = mock.Mock()
        self.app.loop = self.loop
        self.app.on_response_prepare = signals.Signal(self.app)
        req = Request(self.app, message, self.payload,
                      self.transport, self.reader, self.writer)
        return req

    def test_concurrent_receive(self):
        req = self.make_request('GET', '/')
        ws = WebSocketResponse()
        self.loop.run_until_complete(ws.prepare(req))
        ws._waiting = True
        self.assertRaises(
            RuntimeError, self.loop.run_until_complete, ws.receive())