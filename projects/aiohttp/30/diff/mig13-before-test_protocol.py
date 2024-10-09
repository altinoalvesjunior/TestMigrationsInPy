import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_add_headers(self):
        msg = protocol.Response(self.transport, 200)
        self.assertEqual([], list(msg.headers))

        msg.add_headers(('content-type', 'plain/html'))
        self.assertEqual(
            [('CONTENT-TYPE', 'plain/html')], list(msg.headers.items()))