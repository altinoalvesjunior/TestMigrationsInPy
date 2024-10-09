import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_dont_override_response_headers_with_default_values(self):
        msg = protocol.Response(self.transport, 200, http_version=(1, 0))
        msg.add_header('DATE', 'now')
        msg.add_header('SERVER', 'custom')
        msg._add_default_headers()
        self.assertEqual('custom', msg.headers['SERVER'])
        self.assertEqual('now', msg.headers['DATE'])