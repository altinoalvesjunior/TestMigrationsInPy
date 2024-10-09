import unittest
from unittest import mock
import zlib
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()
        self._comp = zlib.compressobj(wbits=-zlib.MAX_WBITS)
        self._COMPRESSED = b''.join([self._comp.compress(b'data'), self._comp.flush()])

    def test_write_payload_deflate_filter(self):
        write = self.transport.write = mock.Mock()
        msg = protocol.Response(self.transport, 200)
        msg.add_headers(('content-length', '{}'.format(len(self._COMPRESSED))))
        msg.send_headers()

        msg.add_compression_filter('deflate')
        msg.write(b'data')
        msg.write_eof()

        chunks = [c[1][0] for c in list(write.mock_calls)]
        self.assertTrue(all(chunks))
        content = b''.join(chunks)
        self.assertEqual(
            self._COMPRESSED, content.split(b'\r\n\r\n', 1)[-1])