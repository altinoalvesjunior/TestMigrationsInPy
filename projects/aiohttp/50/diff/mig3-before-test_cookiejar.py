import asyncio
import gc
import ssl
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

    def test_respect_precreated_ssl_context(self):
        ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        conn = aiohttp.TCPConnector(loop=self.loop, ssl_context=ctx)
        self.assertIs(ctx, conn.ssl_context)