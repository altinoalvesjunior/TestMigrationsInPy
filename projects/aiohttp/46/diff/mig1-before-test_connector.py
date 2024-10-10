import asyncio
import gc
import os.path
import socket
import unittest
from unittest import mock
import aiohttp
from aiohttp.client import ClientResponse

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

    @asyncio.coroutine
    def test_tcp_connector_resolve_host_use_dns_cache(self):
        conn = aiohttp.TCPConnector(loop=self.loop, use_dns_cache=True)

        res = yield from conn._resolve_host('localhost', 8080)
        self.assertTrue(res)
        for rec in res:
            if rec['family'] == socket.AF_INET:
                self.assertEqual(rec['host'], '127.0.0.1')
                self.assertEqual(rec['hostname'], 'localhost')
                self.assertEqual(rec['port'], 8080)
            elif rec['family'] == socket.AF_INET6:
                self.assertEqual(rec['host'], '::1')
                self.assertEqual(rec['hostname'], 'localhost')
                self.assertEqual(rec['port'], 8080)