import asyncio
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

class TestWebRequest(unittest.TestCase):
    def test_doubleslashes(self):
        req = self.make_request('GET', '//foo/')
        self.assertEqual('//foo/', req.path)