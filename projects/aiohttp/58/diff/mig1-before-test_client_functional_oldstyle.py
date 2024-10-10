import asyncio
import unittest
import aiohttp
from aiohttp import client, test_utils, web
from aiohttp.test_utils import run_briefly, unused_port

class TestHttpClientFunctional(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        test_utils.run_briefly(self.loop)
        self.loop.close()
        gc.collect()

    def test_dont_close_explicit_connector(self):
        async def go(url):
            connector = aiohttp.TCPConnector(loop=self.loop)
            session = client.ClientSession(loop=self.loop, connector=connector)
            r = await session.request('GET', url)
            await r.read()
            self.assertEqual(1, len(connector._conns))
            connector.close()
            await session.close()
        with run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('keepalive')
            self.loop.run_until_complete(go(url))