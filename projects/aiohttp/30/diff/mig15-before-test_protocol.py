import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_add_headers_upgrade(self):
        msg = protocol.Response(self.transport, 200)
        self.assertFalse(msg.upgrade)

        msg.add_headers(('connection', 'upgrade'))
        self.assertTrue(msg.upgrade)