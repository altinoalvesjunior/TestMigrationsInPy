import asyncio
import gc
import unittest
from unittest import mock
import aiohttp
from aiohttp import ClientResponse

class TestBaseConnector(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.transport = unittest.mock.Mock()
        self.stream = aiohttp.StreamParser()
        self.response = ClientResponse('get', 'http://base-conn.org')
        self.response._post_init(self.loop)

    def tearDown(self):
        self.response.close()
        self.loop.close()
        gc.collect()

    def test_tcp_connector_ctor_fingerprint_valid(self):
        valid = b'\xa2\x06G\xad\xaa\xf5\xd8\\J\x99^by;\x06='
        conn = aiohttp.TCPConnector(loop=self.loop, fingerprint=valid)
        self.assertEqual(conn.fingerprint, valid)