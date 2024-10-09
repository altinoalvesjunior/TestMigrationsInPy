import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_add_headers_length(self):
        msg = protocol.Response(self.transport, 200)
        self.assertIsNone(msg.length)

        msg.add_headers(('content-length', '42'))
        self.assertEqual(42, msg.length)