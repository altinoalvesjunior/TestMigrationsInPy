import unittest
from aiohttp import WebSocketResponse
from aiohttp.test_utils import make_mocked_request
from aiohttp import CIMultiDict

class TestWebWebSocket(unittest.TestCase):

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

    def test_can_prepare_ok(self):
        req = self.make_request('GET', '/', protocols=True)
        ws = WebSocketResponse(protocols=('chat',))
        self.assertEqual((True, 'chat'), ws.can_prepare(req))