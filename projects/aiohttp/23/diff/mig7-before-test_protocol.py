import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_keep_alive(self):
        msg = protocol.Response(self.transport, 200, close=True)
        self.assertFalse(msg.keep_alive())
        msg.keepalive = True
        self.assertTrue(msg.keep_alive())

        msg.force_close()
        self.assertFalse(msg.keep_alive())