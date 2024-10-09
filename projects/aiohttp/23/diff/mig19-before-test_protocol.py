import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_default_headers(self):
        msg = protocol.Response(self.transport, 200)
        msg._add_default_headers()

        headers = [r for r, _ in msg.headers.items()]
        self.assertIn('DATE', headers)
        self.assertIn('CONNECTION', headers)