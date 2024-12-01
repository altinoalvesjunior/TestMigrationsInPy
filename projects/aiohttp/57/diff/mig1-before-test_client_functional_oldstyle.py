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
    def test_request_conn_closed(self):
        with run_server(self.loop, router=Functional) as httpd:
            httpd['close'] = True
            session = client.ClientSession(loop=self.loop)
            with self.assertRaises(aiohttp.ServerDisconnectedError):
                self.loop.run_until_complete(
                    session.request('get', httpd.url('method', 'get')))
            self.loop.run_until_complete(session.close())