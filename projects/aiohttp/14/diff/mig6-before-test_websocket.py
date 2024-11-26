import unittest
from unittest import mock
from aiohttp import websocket, multidict, protocol, errors

class TestWebSocketHandshake(unittest.TestCase):
    def setUp(self):
        self.transport = mock.Mock()
        self.headers = multidict.MultiDict()
        self.message = protocol.RawRequestMessage(
            'GET', '/path', (1, 0), self.headers, True, None)

    def test_handshake(self):
        hdrs, sec_key = gen_ws_headers()
        self.headers.extend(hdrs)
        status, headers, parser, writer, protocol = websocket.do_handshake(
            self.message.method, self.message.headers, self.transport)
        self.assertEqual(status, 101)
        self.assertIsNone(protocol)