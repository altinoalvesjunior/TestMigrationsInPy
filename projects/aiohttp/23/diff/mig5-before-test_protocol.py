import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_force_close(self):
        msg = protocol.Response(self.transport, 200)
        self.assertFalse(msg.closing)
        msg.force_close()
        self.assertTrue(msg.closing)