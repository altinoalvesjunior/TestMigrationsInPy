import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_write_auto_send_headers(self):
        msg = protocol.Response(self.transport, 200, http_version=(1, 0))
        msg._send_headers = True

        msg.write(b'data1')
        self.assertTrue(msg.headers_sent)
        # cleanup
        msg.writer.close()