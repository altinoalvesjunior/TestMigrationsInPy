import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_force_chunked(self):
        msg = protocol.Response(self.transport, 200)
        self.assertFalse(msg.chunked)
        msg.enable_chunked_encoding()
        self.assertTrue(msg.chunked)