import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_add_headers_upgrade_websocket(self):
        msg = protocol.Response(self.transport, 200)

        msg.add_headers(('upgrade', 'test'))
        self.assertEqual([], list(msg.headers))

        msg.add_headers(('upgrade', 'websocket'))
        self.assertEqual(
            [('UPGRADE', 'websocket')], list(msg.headers.items()))