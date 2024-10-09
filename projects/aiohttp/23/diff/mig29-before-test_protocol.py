import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_prepare_chunked_force(self):
        msg = protocol.Response(self.transport, 200)
        msg.enable_chunked_encoding()

        chunked = msg._write_chunked_payload = mock.Mock()
        chunked.return_value = iter([1, 2, 3])

        msg.add_headers(('content-length', '42'))
        msg.send_headers()
        self.assertTrue(chunked.called)