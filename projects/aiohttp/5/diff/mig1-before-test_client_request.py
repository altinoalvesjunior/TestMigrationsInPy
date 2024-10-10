import asyncio
import gc
import unittest
import unittest.mock

import inspect
import io
import urllib.parse
import os.path

from http.cookies import SimpleCookie

import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse
from aiohttp.multidict import upstr, CIMultiDict, CIMultiDictProxy
from aiohttp import BaseConnector


class TestClientRequest(unittest.TestCase):
    def test_method(self):
        req = ClientRequest('get', 'http://python.org/', loop=self.loop)
        self.assertEqual(req.method, 'GET')
        self.loop.run_until_complete(req.close())
        req = ClientRequest('head', 'http://python.org/', loop=self.loop)
        self.assertEqual(req.method, 'HEAD')
        self.loop.run_until_complete(req.close())
        req = ClientRequest('HEAD', 'http://python.org/', loop=self.loop)
        self.assertEqual(req.method, 'HEAD')
        self.loop.run_until_complete(req.close())