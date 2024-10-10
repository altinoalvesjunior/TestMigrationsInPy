import asyncio
import binascii
import gc
import http.cookies
import io
import json
import os.path
import unittest
from unittest import mock

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

    def test_POST_FILES_SINGLE_BINARY(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('method', 'post')
            here = os.path.dirname(__file__)
            fname = os.path.join(here, 'sample.key')
            with open(fname, 'rb') as f:
                r = self.loop.run_until_complete(
                    client.request('post', url, data=f, loop=self.loop))
                content = self.loop.run_until_complete(r.json())
                f.seek(0)
                self.assertEqual(0, len(content['multipart-data']))
                self.assertEqual(content['content'], f.read().decode())
                self.assertIn(content['headers']['Content-Type'],
                              ('application/pgp-keys',
                               'application/octet-stream'))
                self.assertEqual(r.status, 200)
                r.close()