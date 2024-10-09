import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_write_drain(self):
        msg = protocol.Response(self.transport, 200, http_version=(1, 0))
        msg._send_headers = True

        msg.write(b'1' * (64 * 1024 * 2))
        self.assertFalse(self.transport.drain.called)

        msg.write(b'1', drain=True)
        self.assertTrue(self.transport.drain.called)
        self.assertEqual(msg._output_size, 0)