import asyncio
import pytest
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

def test_POST(make_request):
    req = make_request('POST', '/')
    with pytest.raises(RuntimeError):
        req.POST
    marker = object()
    req._post = marker
    assert req.POST is marker
    assert req.POST is marker