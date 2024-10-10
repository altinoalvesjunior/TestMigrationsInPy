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

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        test_utils.run_briefly(self.loop)
        self.loop.close()
        gc.collect()

    def test_POST_FILES_IO_WITH_PARAMS(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('method', 'post')
            data = io.BytesIO(b'data')
            r = self.loop.run_until_complete(
                client.request('post', url,
                               data=(('test', 'true'),
                                     MultiDict(
                                         [('q', 't1'), ('q', 't2')]),
                                     data),
                               loop=self.loop))
            content = self.loop.run_until_complete(r.json())
            self.assertEqual(4, len(content['multipart-data']))
            self.assertEqual(
                {'content-type': 'text/plain',
                 'data': 'true',
                 'name': 'test'}, content['multipart-data'][0])
            self.assertEqual(
                {'content-type': 'application/octet-stream',
                 'data': 'data',
                 'filename': 'unknown',
                 'filename*': "utf-8''unknown",
                 'name': 'unknown'}, content['multipart-data'][1])
            self.assertEqual(
                {'content-type': 'text/plain',
                 'data': 't1',
                 'name': 'q'}, content['multipart-data'][2])
            self.assertEqual(
                {'content-type': 'text/plain',
                 'data': 't2',
                 'name': 'q'}, content['multipart-data'][3])
            self.assertEqual(r.status, 200)
            r.close()