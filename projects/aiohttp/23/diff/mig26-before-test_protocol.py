import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_send_headers_non_ascii(self):
        write = self.transport.write = mock.Mock()

        msg = protocol.Response(self.transport, 200)
        msg.add_headers(('x-header', 'текст'))
        self.assertFalse(msg.is_headers_sent())

        msg.send_headers()

        content = b''.join([arg[1][0] for arg in list(write.mock_calls)])

        self.assertTrue(content.startswith(b'HTTP/1.1 200 OK\r\n'))
        self.assertIn(b'X-HEADER: \xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82',
                      content)
        self.assertTrue(msg.headers_sent)
        self.assertTrue(msg.is_headers_sent())
        # cleanup
        msg.writer.close()