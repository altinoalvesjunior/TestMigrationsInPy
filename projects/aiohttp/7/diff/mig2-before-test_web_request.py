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
    def test_calc_content_type_on_getting_charset(self):
        req = self.make_request(
            'Get', '/',
            CIMultiDict([('CONTENT-TYPE', 'text/html; charset=UTF-8')]))
        self.assertEqual('UTF-8', req.charset)
        self.assertEqual('text/html', req.content_type)