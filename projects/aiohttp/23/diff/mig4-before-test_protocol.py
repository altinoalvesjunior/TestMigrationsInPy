import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_start_response_with_unknown_reason(self):
        msg = protocol.Response(self.transport, 777, close=True)

        self.assertEqual(msg.status, 777)
        self.assertEqual(msg.reason, "777")
        self.assertEqual(msg.status_line, 'HTTP/1.1 777 777\r\n')
        
