import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_add_header_invalid_value_type(self):
        msg = protocol.Response(self.transport, 200)
        self.assertEqual([], list(msg.headers))

        with self.assertRaises(AssertionError):
            msg.add_header('content-type', {'test': 'plain'})

        with self.assertRaises(AssertionError):
            msg.add_header(list('content-type'), 'text/plain')