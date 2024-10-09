import unittest
from unittest import mock
from aiohttp import protocol

class TestHttpMessage(unittest.TestCase):

    def setUp(self):
        self.transport = mock.Mock()

    def test_add_header_non_ascii(self):
        msg = protocol.Response(self.transport, 200)
        self.assertEqual([], list(msg.headers))

        with self.assertRaises(AssertionError):
            msg.add_header('тип-контента', 'текст/плейн')