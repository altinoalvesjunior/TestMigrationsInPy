import asyncio
import pytest
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

def test_call_POST_on_weird_content_type(make_request):
    req = make_request(
        'POST', '/',
        headers=CIMultiDict({'CONTENT-TYPE': 'something/weird'}))
    ret = yield from req.post()
    assert CIMultiDict() == ret