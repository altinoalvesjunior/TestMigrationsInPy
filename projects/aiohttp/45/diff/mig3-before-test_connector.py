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

    def test_del_with_closed_loop(self):
        conn = aiohttp.BaseConnector(loop=self.loop)
        transp = unittest.mock.Mock()
        conn._conns['a'] = [(transp, 'proto', 123)]

        conns_impl = conn._conns
        conn._start_cleanup_task()
        exc_handler = unittest.mock.Mock()
        self.loop.set_exception_handler(exc_handler)
        self.loop.close()

        with self.assertWarns(ResourceWarning):
            del conn
            gc.collect()

        self.assertFalse(conns_impl)
        self.assertFalse(transp.close.called)
        self.assertTrue(exc_handler.called)