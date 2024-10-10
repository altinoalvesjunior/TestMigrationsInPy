import asyncio
import gc
import unittest
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

    def test_close_twice(self):
        tr = unittest.mock.Mock()

        conn = aiohttp.BaseConnector(loop=self.loop)
        conn._conns[1] = [(tr, object(), object())]
        conn.close()

        self.assertFalse(conn._conns)
        self.assertTrue(tr.close.called)
        self.assertTrue(conn.closed)

        conn._conns = 'Invalid'  # fill with garbage
        conn.close()
        self.assertTrue(conn.closed)