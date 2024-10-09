import asyncio
import unittest
from aiohttp import WebSocketResponse
from aiohttp.test_utils import make_mocked_request

class TestWebWebSocket(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def make_request(self, method, path, headers=None, protocols=False):
        if headers is None:
            headers = {
                'HOST': 'server.example.com',
                'UPGRADE': 'websocket',
                'CONNECTION': 'Upgrade',
                'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==',
                'ORIGIN': 'http://example.com',
                'SEC-WEBSOCKET-VERSION': '13'
            }
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers)

    def test_write_eof_idempotent(self):
        req = self.make_request('GET', '/')
        ws = WebSocketResponse()
        self.loop.run_until_complete(ws.prepare(req))
        self.loop.run_until_complete(ws.close())
        @asyncio.coroutine
        def go():
            yield from ws.write_eof()
            yield from ws.write_eof()
            yield from ws.write_eof()
        self.loop.run_until_complete(go())