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
    def test_non_keepalive_on_http10(self):
        req = self.make_request('GET', '/', version=HttpVersion(1, 0))
        self.assertFalse(req.keep_alive)