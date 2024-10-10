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

    def test_HTTP_307_REDIRECT_POST(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            r = self.loop.run_until_complete(
                client.request('post', httpd.url('redirect_307', 2),
                               data={'some': 'data'}, loop=self.loop))
            content = self.loop.run_until_complete(r.content.read())
            content = content.decode()
            self.assertEqual(r.status, 200)
            self.assertIn('"method": "POST"', content)
            self.assertEqual(2, httpd['redirects'])
            r.close()