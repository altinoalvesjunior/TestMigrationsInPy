import unittest
from unittest import mock
from aiohttp import websocket, multidict, protocol, errors

class TestWebSocketHandshake(unittest.TestCase):
    def setUp(self):
        self.transport = mock.Mock()
        self.headers = multidict.MultiDict()
        self.message = protocol.RawRequestMessage(
            'GET', '/path', (1, 0), self.headers, True, None)

    def test_not_get(self):
        self.assertRaises(
            errors.HttpProcessingError,
            websocket.do_handshake,
            'POST', self.message.headers, self.transport
        )