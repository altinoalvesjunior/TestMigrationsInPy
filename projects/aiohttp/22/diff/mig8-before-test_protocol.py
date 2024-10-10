import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_dont_override_request_headers_with_default_values(self):
        msg = protocol.Request(
            self.transport, 'GET', '/index.html', close=True)
        msg.add_header('USER-AGENT', 'custom')
        msg._add_default_headers()
        self.assertEqual('custom', msg.headers['USER-AGENT'])