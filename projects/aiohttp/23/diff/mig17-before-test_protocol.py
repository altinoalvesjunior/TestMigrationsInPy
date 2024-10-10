import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_add_headers_connection_keepalive(self):
        msg = protocol.Response(self.transport, 200)

        msg.add_headers(('connection', 'keep-alive'))
        self.assertEqual([], list(msg.headers))
        self.assertTrue(msg.keepalive)

        msg.add_headers(('connection', 'close'))
        self.assertFalse(msg.keepalive)