import asyncio
import binascii
import gc
import http.cookies
import json
import os.path
import unittest
from unittest import mock

from multidict import MultiDict

import aiohttp
from aiohttp import client, helpers, test_utils
from aiohttp.multipart import MultipartWriter
from aiohttp.test_utils import unused_port


class TestHttpClientFunctional(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        test_utils.run_briefly(self.loop)
        self.loop.close()
        gc.collect()

    def test_expect_continue(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('method', 'post')
            r = self.loop.run_until_complete(
                client.request('post', url, data={'some': 'data'},
                               expect100=True, loop=self.loop))
            self.assertEqual(r.status, 200)
            content = self.loop.run_until_complete(r.json())
            self.assertEqual('100-continue', content['headers']['Expect'])
            self.assertEqual(r.status, 200)
            r.close()