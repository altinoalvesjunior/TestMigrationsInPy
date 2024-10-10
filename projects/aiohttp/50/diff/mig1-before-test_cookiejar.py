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

    def test_ambigous_verify_ssl_and_ssl_context(self):
        with self.assertRaises(ValueError):
            aiohttp.TCPConnector(
                verify_ssl=False,
                ssl_context=ssl.SSLContext(ssl.PROTOCOL_SSLv23),
                loop=self.loop)