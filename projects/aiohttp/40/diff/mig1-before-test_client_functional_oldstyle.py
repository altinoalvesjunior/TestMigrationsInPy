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

    def test_POST_FILES_WITH_DATA(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('method', 'post')
            here = os.path.dirname(__file__)
            fname = os.path.join(here, 'sample.key')
            with open(fname) as f:
                r = self.loop.run_until_complete(
                    client.request('post', url, loop=self.loop,
                                   data={'test': 'true', 'some': f}))
                content = self.loop.run_until_complete(r.json())
                files = list(
                    sorted(content['multipart-data'],
                           key=lambda d: d['name']))
                self.assertEqual(2, len(content['multipart-data']))
                self.assertEqual('test', files[1]['name'])
                self.assertEqual('true', files[1]['data'])
                f.seek(0)
                filename = os.path.split(f.name)[-1]
                self.assertEqual('some', files[0]['name'])
                self.assertEqual(filename, files[0]['filename'])
                self.assertEqual(f.read(), files[0]['data'])
                self.assertEqual(r.status, 200)
                r.close()