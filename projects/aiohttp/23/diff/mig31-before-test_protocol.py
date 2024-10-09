import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_prepare_eof(self):
        msg = protocol.Response(self.transport, 200, http_version=(1, 0))

        eof = msg._write_eof_payload = mock.Mock()
        eof.return_value = iter([1, 2, 3])

        msg.send_headers()
        self.assertTrue(eof.called)