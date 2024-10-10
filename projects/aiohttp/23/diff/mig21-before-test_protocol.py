import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_default_headers_chunked(self):
        msg = protocol.Response(self.transport, 200)
        msg._add_default_headers()

        headers = [r for r, _ in msg.headers.items()]
        self.assertNotIn('TRANSFER-ENCODING', headers)

        msg = protocol.Response(self.transport, 200)
        msg.enable_chunked_encoding()
        msg.send_headers()

        headers = [r for r, _ in msg.headers.items()]
        self.assertIn('TRANSFER-ENCODING', headers)