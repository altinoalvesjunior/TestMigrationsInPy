import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_start_request(self):
        msg = protocol.Request(
            self.transport, 'GET', '/index.html', close=True)

        self.assertIs(msg.transport, self.transport)
        self.assertTrue(msg.closing)
        self.assertEqual(msg.status_line, 'GET /index.html HTTP/1.1\r\n')