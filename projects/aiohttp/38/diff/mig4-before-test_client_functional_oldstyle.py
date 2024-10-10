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

    def test_POST_FILES_LIST_CT(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('method', 'post')
            here = os.path.dirname(__file__)
            fname = os.path.join(here, 'sample.key')
            with open(fname) as f:
                form = aiohttp.FormData()
                form.add_field('some', f, content_type='text/plain')
                r = self.loop.run_until_complete(
                    client.request('post', url, loop=self.loop,
                                   data=form))
                content = self.loop.run_until_complete(r.json())
                f.seek(0)
                filename = os.path.split(f.name)[-1]
                self.assertEqual(1, len(content['multipart-data']))
                self.assertEqual(
                    'some', content['multipart-data'][0]['name'])
                self.assertEqual(
                    filename, content['multipart-data'][0]['filename'])
                self.assertEqual(
                    f.read(), content['multipart-data'][0]['data'])
                self.assertEqual(
                    'text/plain', content['multipart-data'][0]['content-type'])
                self.assertEqual(r.status, 200)
                r.close()