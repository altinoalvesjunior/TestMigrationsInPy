import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_default_headers_server(self):
        msg = protocol.Response(self.transport, 200)
        msg._add_default_headers()

        self.assertIn('SERVER', msg.headers)