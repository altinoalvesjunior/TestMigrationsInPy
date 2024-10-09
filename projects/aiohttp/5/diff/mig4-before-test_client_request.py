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
    def test_host_port(self):
        req = ClientRequest('get', 'http://python.org/', loop=self.loop)
        self.assertEqual(req.host, 'python.org')
        self.assertEqual(req.port, 80)
        self.assertFalse(req.ssl)
        self.loop.run_until_complete(req.close())
        req = ClientRequest('get', 'https://python.org/', loop=self.loop)
        self.assertEqual(req.host, 'python.org')
        self.assertEqual(req.port, 443)
        self.assertTrue(req.ssl)
        self.loop.run_until_complete(req.close())
        req = ClientRequest('get', 'https://python.org:960/', loop=self.loop)
        self.assertEqual(req.host, 'python.org')
        self.assertEqual(req.port, 960)
        self.assertTrue(req.ssl)
        self.loop.run_until_complete(req.close())