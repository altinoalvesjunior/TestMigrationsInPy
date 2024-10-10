import unittest
from unittest import mock
from aiohttp import hdrs, protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_add_headers_hop_headers(self):
        msg = protocol.Response(self.transport, 200)
        msg.HOP_HEADERS = (hdrs.TRANSFER_ENCODING,)

        msg.add_headers(('connection', 'test'), ('transfer-encoding', 't'))
        self.assertEqual([], list(msg.headers))