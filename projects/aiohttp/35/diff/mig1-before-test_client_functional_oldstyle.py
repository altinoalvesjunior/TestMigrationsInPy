import asyncio
import unittest
from unittest import mock
import aiohttp
from aiohttp import client, test_utils

class TestHttpClientFunctional(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        test_utils.run_briefly(self.loop)
        self.loop.close()

    def test_HTTP_302_REDIRECT_NON_HTTP(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            @asyncio.coroutine
            def go():
                with self.assertRaises(ValueError):
                    yield from client.request('get',
                                              httpd.url('redirect_err'),
                                              loop=self.loop)
            self.loop.run_until_complete(go())