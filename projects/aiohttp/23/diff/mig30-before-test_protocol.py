import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_prepare_chunked_no_length(self):
        msg = protocol.Response(self.transport, 200)

        chunked = msg._write_chunked_payload = mock.Mock()
        chunked.return_value = iter([1, 2, 3])

        msg.send_headers()
        self.assertTrue(chunked.called)