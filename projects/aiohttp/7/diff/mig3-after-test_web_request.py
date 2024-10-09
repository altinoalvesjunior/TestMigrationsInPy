import asyncio
import pytest
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

def test_urlencoded_querystring(make_request):
    req = make_request('GET',
                       '/yandsearch?text=%D1%82%D0%B5%D0%BA%D1%81%D1%82')
    assert {'text': 'текст'} == req.GET