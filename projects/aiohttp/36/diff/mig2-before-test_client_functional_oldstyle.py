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

    def test_POST_DATA_with_explicit_formdata(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('method', 'post')
            form = aiohttp.FormData()
            form.add_field('name', 'text')
            r = self.loop.run_until_complete(
                client.request('post', url,
                               data=form,
                               loop=self.loop))
            self.assertEqual(r.status, 200)
            content = self.loop.run_until_complete(r.json())
            self.assertEqual({'name': ['text']}, content['form'])
            self.assertEqual(r.status, 200)
            r.close()