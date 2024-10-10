import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_send_headers(self):
        write = self.transport.write = mock.Mock()

        msg = protocol.Response(self.transport, 200)
        msg.add_headers(('content-type', 'plain/html'))
        self.assertFalse(msg.is_headers_sent())

        msg.send_headers()

        content = b''.join([arg[1][0] for arg in list(write.mock_calls)])

        self.assertTrue(content.startswith(b'HTTP/1.1 200 OK\r\n'))
        self.assertIn(b'CONTENT-TYPE: plain/html', content)
        self.assertTrue(msg.headers_sent)
        self.assertTrue(msg.is_headers_sent())
        # cleanup
        msg.writer.close()