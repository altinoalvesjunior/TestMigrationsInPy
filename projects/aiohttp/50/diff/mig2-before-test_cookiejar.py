import asyncio
import gc
import unittest
import aiohttp
from aiohttp import ClientResponse

class TestCookieJarBase(unittest.TestCase):

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

    def test_dont_recreate_ssl_context(self):
        conn = aiohttp.TCPConnector(loop=self.loop)
        ctx = conn.ssl_context
        self.assertIs(ctx, conn.ssl_context)