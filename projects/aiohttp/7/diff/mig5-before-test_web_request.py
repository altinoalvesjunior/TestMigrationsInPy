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
    def test_content_length(self):
        req = self.make_request(
            'Get', '/',
            CIMultiDict([('CONTENT-LENGTH', '123')]))
        self.assertEqual(123, req.content_length)