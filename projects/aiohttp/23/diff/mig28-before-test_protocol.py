import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_prepare_length(self):
        msg = protocol.Response(self.transport, 200)
        w_l_p = msg._write_length_payload = mock.Mock()
        w_l_p.return_value = iter([1, 2, 3])

        msg.add_headers(('content-length', '42'))
        msg.send_headers()

        self.assertTrue(w_l_p.called)
        self.assertEqual((42,), w_l_p.call_args[0])