import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_start_response_with_reason(self):
        msg = protocol.Response(self.transport, 333, close=True,
                                reason="My Reason")

        self.assertEqual(msg.status, 333)
        self.assertEqual(msg.reason, "My Reason")
        self.assertEqual(msg.status_line, 'HTTP/1.1 333 My Reason\r\n')