import asyncio
import pytest
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

class TestWebRequest(unittest.TestCase):
    def test_call_POST_on_GET_request(self):
        req = self.make_request('GET', '/')
        ret = self.loop.run_until_complete(req.post())
        self.assertEqual(CIMultiDict(), ret)