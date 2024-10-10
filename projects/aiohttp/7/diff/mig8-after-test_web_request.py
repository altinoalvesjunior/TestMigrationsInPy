import asyncio
import pytest
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

@pytest.mark.run_loop
def test_call_POST_on_GET_request(make_request):
    req = make_request('GET', '/')
    ret = yield from req.post()
    assert CIMultiDict() == ret