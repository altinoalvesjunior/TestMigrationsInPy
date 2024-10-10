import asyncio
import binascii
import gc
import http.cookies
import io
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
    def test_use_global_loop(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            try:
                asyncio.set_event_loop(self.loop)
                r = self.loop.run_until_complete(
                    client.request('get', httpd.url('method', 'get')))
            finally:
                asyncio.set_event_loop(None)
            content1 = self.loop.run_until_complete(r.read())
            content2 = self.loop.run_until_complete(r.read())
            content = content1.decode()
            self.assertEqual(r.status, 200)
            self.assertIn('"method": "GET"', content)
            self.assertEqual(content1, content2)
            r.close()
    def test_HTTP_302_REDIRECT_GET(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            @asyncio.coroutine
            def go():
                r = yield from client.request('get',
                                              httpd.url('redirect', 2),
                                              loop=self.loop)
                self.assertEqual(r.status, 200)
                self.assertEqual(2, httpd['redirects'])
                r.close()
            self.loop.run_until_complete(go())