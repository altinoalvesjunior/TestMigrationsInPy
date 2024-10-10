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

    def test_close_cancels_cleanup_handle(self):
        conn = aiohttp.BaseConnector(loop=self.loop)
        conn._start_cleanup_task()

        self.assertIsNotNone(conn._cleanup_handle)
        conn.close()
        self.assertIsNone(conn._cleanup_handle)