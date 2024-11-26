import unittest
from unittest import mock
from aiohttp import websocket, multidict, protocol, errors

class TestWebSocketHandshake(unittest.TestCase):
    def setUp(self):
        self.transport = mock.Mock()
        self.headers = multidict.MultiDict()
        self.message = protocol.RawRequestMessage(
            'GET', '/path', (1, 0), self.headers, True, None)

    @mock.patch('aiohttp.websocket.ws_logger.warning')
    def test_handshake_protocol_unsupported(self, m_websocket_warn):
        proto = 'chat'
        self.headers.extend(gen_ws_headers('test')[0])
        _, _, _, _, protocol = websocket.do_handshake(
            self.message.method, self.message.headers, self.transport,
            protocols=[proto])
        self.assertIsNone(protocol)