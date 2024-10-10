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

    def test_tcp_connector_ctor(self):
        conn = aiohttp.TCPConnector(loop=self.loop)
        self.assertTrue(conn.verify_ssl)
        self.assertIs(conn.fingerprint, None)
        with self.assertWarns(DeprecationWarning):
            self.assertFalse(conn.resolve)
        self.assertFalse(conn.use_dns_cache)
        self.assertEqual(conn.family, 0)
        with self.assertWarns(DeprecationWarning):
            self.assertEqual(conn.resolved_hosts, {})
        self.assertEqual(conn.resolved_hosts, {})