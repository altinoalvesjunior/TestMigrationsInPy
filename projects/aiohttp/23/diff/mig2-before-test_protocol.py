import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_start_response(self):
        msg = protocol.Response(self.transport, 200, close=True)

        self.assertIs(msg.transport, self.transport)
        self.assertEqual(msg.status, 200)
        self.assertEqual(msg.reason, "OK")
        self.assertTrue(msg.closing)
        self.assertEqual(msg.status_line, 'HTTP/1.1 200 OK\r\n')