import unittest
from unittest import mock
from aiohttp import websocket, multidict, protocol, errors

class TestWebSocketHandshake(unittest.TestCase):
    def setUp(self):
        self.transport = mock.Mock()
        self.headers = multidict.MultiDict()
        self.message = protocol.RawRequestMessage(
            'GET', '/path', (1, 0), self.headers, True, None)

    def test_no_connection(self):
        self.headers.extend([('UPGRADE', 'websocket'),
                             ('CONNECTION', 'keep-alive')])
        self.assertRaises(
            errors.HttpBadRequest,
            websocket.do_handshake,
            self.message.method, self.message.headers, self.transport
        )