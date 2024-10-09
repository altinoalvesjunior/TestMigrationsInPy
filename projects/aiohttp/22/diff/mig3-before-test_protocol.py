import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_write_payload_chunked_large_chunk(self):
        write = self.transport.write = mock.Mock()
        msg = protocol.Response(self.transport, 200)
        msg.send_headers()

        msg.add_chunking_filter(1024)
        msg.write(b'data')
        msg.write_eof()
        content = b''.join([c[1][0] for c in list(write.mock_calls)])
        self.assertTrue(content.endswith(b'4\r\ndata\r\n0\r\n\r\n'))