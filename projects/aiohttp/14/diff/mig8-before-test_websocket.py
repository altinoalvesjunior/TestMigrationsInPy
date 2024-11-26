import unittest
from unittest import mock
from aiohttp import websocket, multidict, protocol, errors

class TestWebSocketHandshake(unittest.TestCase):
    def setUp(self):
        self.transport = mock.Mock()
        self.headers = multidict.MultiDict()
        self.message = protocol.RawRequestMessage(
            'GET', '/path', (1, 0), self.headers, True, None)

    def test_handshake_protocol_agreement(self):
        best_proto = 'worse_proto'
        wanted_protos = ['best', 'chat', 'worse_proto']
        server_protos = 'worse_proto,chat'
        self.headers.extend(gen_ws_headers(server_protos)[0])
        _, resp_headers, _, _, protocol = websocket.do_handshake(
            self.message.method, self.message.headers, self.transport,
            protocols=wanted_protos)
        self.assertEqual(protocol, best_proto)