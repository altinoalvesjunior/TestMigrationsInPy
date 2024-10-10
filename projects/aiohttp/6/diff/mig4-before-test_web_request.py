import asyncio
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

class TestWebRequest(unittest.TestCase):
    def test_content_type_not_specified(self):
        req = self.make_request('Get', '/')
        self.assertEqual('application/octet-stream', req.content_type)