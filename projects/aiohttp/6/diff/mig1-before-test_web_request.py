import asyncio
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

class TestWebRequest(unittest.TestCase):
    def test_ctor(self):
        req = self.make_request('GET', '/path/to?a=1&b=2')
        self.assertIs(self.app, req.app)
        self.assertEqual('GET', req.method)
        self.assertEqual(HttpVersion(1, 1), req.version)
        self.assertEqual(None, req.host)
        self.assertEqual('/path/to?a=1&b=2', req.path_qs)
        self.assertEqual('/path/to', req.path)
        self.assertEqual('a=1&b=2', req.query_string)
        get = req.GET
        self.assertEqual(MultiDict([('a', '1'), ('b', '2')]), get)
        # second call should return the same object
        self.assertIs(get, req.GET)
        with self.assertWarns(DeprecationWarning):
            self.assertIs(self.payload, req.payload)
        self.assertIs(self.payload, req.content)
        self.assertIs(self.transport, req.transport)
        self.assertTrue(req.keep_alive)