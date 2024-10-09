import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_send_headers_nomore_add(self):
        msg = protocol.Response(self.transport, 200)
        msg.add_headers(('content-type', 'plain/html'))
        msg.send_headers()

        self.assertRaises(AssertionError,
                          msg.add_header, 'content-type', 'plain/html')
        # cleanup
        msg.writer.close()