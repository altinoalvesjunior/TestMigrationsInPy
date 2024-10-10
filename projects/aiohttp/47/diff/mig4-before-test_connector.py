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

    def test_tcp_connector_clear_resolved_hosts(self):
        conn = aiohttp.TCPConnector(loop=self.loop)
        info = object()
        conn._cached_hosts[('localhost', 123)] = info
        conn._cached_hosts[('localhost', 124)] = info
        conn.clear_resolved_hosts('localhost', 123)
        self.assertEqual(
            conn.resolved_hosts, {('localhost', 124): info})
        conn.clear_resolved_hosts('localhost', 123)
        self.assertEqual(
            conn.resolved_hosts, {('localhost', 124): info})
        with self.assertWarns(DeprecationWarning):
            conn.clear_resolved_hosts()
        self.assertEqual(conn.resolved_hosts, {})