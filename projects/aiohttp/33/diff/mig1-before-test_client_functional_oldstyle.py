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
    def test_HTTP_200_OK_METHOD(self):
        with test_utils.run_server(self.loop, router=Functional) as httpd:
            for meth in ('get', 'post', 'put', 'delete', 'head'):
                r = self.loop.run_until_complete(
                    client.request(meth, httpd.url('method', meth),
                                   loop=self.loop))
                content1 = self.loop.run_until_complete(r.read())
                content2 = self.loop.run_until_complete(r.read())
                content = content1.decode()
                self.assertEqual(r.status, 200)
                if meth == 'head':
                    self.assertEqual(b'', content1)
                else:
                    self.assertIn('"method": "%s"' % meth.upper(), content)
                self.assertEqual(content1, content2)
                r.close()
