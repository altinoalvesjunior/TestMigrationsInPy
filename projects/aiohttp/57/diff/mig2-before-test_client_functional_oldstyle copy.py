import asyncio
import binascii
import cgi
import contextlib
import email.parser
import unittest
import urllib.parse
from http.cookies import SimpleCookie
from unittest import mock
from multidict import MultiDict

import aiohttp
import aiohttp.http
from aiohttp import client, test_utils, web
from aiohttp.multipart import MultipartWriter
from aiohttp.test_utils import run_briefly, unused_port

class TestHttpClientFunctional(unittest.TestCase):
    def test_POST_DATA_with_charset_pub_request(self):
        with run_server(self.loop, router=Functional) as httpd:
            url = httpd.url('method', 'post')
            form = aiohttp.FormData()
            form.add_field('name', 'текст',
                           content_type='text/plain; charset=koi8-r')
            session = client.ClientSession(loop=self.loop)
            r = self.loop.run_until_complete(
                session.request('post', url, data=form))
            content = self.loop.run_until_complete(r.json())
            self.assertEqual(1, len(content['multipart-data']))
            field = content['multipart-data'][0]
            self.assertEqual('name', field['name'])
            self.assertEqual('текст', field['data'])
            self.assertEqual(r.status, 200)
            r.close()
            self.loop.run_until_complete(session.close())