import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_write_payload_eof(self):
        write = self.transport.write = mock.Mock()
        msg = protocol.Response(self.transport, 200, http_version=(1, 0))
        msg.send_headers()

        msg.write(b'data1')
        self.assertTrue(msg.headers_sent)

        msg.write(b'data2')
        msg.write_eof()

        content = b''.join([c[1][0] for c in list(write.mock_calls)])
        self.assertEqual(
            b'data1data2', content.split(b'\r\n\r\n', 1)[-1])