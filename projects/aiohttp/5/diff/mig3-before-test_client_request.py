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
    def test_version_err(self):
        self.assertRaises(
            ValueError,
            ClientRequest, 'get', 'http://python.org/', version='1.c',
            loop=self.loop)