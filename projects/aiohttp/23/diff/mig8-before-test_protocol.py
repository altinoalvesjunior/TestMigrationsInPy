import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_keep_alive_http10(self):
        msg = protocol.Response(self.transport, 200, http_version=(1, 0))
        self.assertFalse(msg.keepalive)
        self.assertFalse(msg.keep_alive())

        msg = protocol.Response(self.transport, 200, http_version=(1, 1))
        self.assertIsNone(msg.keepalive)