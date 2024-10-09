import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_default_headers_connection_close(self):
        msg = protocol.Response(self.transport, 200)
        msg.force_close()
        msg._add_default_headers()

        headers = [r for r in msg.headers.items() if r[0] == 'CONNECTION']
        self.assertEqual([('CONNECTION', 'close')], headers)