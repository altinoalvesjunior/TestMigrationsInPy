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
    def test_version(self):
        req = ClientRequest('get', 'http://python.org/', version='1.0',
                            loop=self.loop)
        self.assertEqual(req.version, (1, 0))
        self.loop.run_until_complete(req.close())