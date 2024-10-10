import asyncio
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

class TestWebRequest(unittest.TestCase):
    def test_POST(self):
        req = self.make_request('POST', '/')
        with self.assertRaises(RuntimeError):
            req.POST
        marker = object()
        req._post = marker
        self.assertIs(req.POST, marker)
        self.assertIs(req.POST, marker)
