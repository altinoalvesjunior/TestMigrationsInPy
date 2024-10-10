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

    def test_POST_DATA_with_content_transfer_encoding(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('method', 'post')

            form = aiohttp.FormData()
            form.add_field('name', b'123',
                           content_transfer_encoding='base64')

            r = self.loop.run_until_complete(
                client.request(
                    'post', url, data=form,
                    loop=self.loop))
            content = self.loop.run_until_complete(r.json())

            self.assertEqual(1, len(content['multipart-data']))
            field = content['multipart-data'][0]
            self.assertEqual('name', field['name'])
            self.assertEqual(b'123', binascii.a2b_base64(field['data']))
            self.assertEqual(r.status, 200)