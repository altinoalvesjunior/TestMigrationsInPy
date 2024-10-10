import asyncio
import pytest
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

def test_ctor(make_request, warning):
    req = make_request('GET', '/path/to?a=1&b=2')
    assert 'GET' == req.method
    assert HttpVersion(1, 1) == req.version
    assert req.host is None
    assert '/path/to?a=1&b=2' == req.path_qs
    assert '/path/to' == req.path
    assert 'a=1&b=2' == req.query_string
    get = req.GET
    assert MultiDict([('a', '1'), ('b', '2')]) == get
    # second call should return the same object
    assert get is req.GET
    with warning(DeprecationWarning):
        req.payload
    assert req.keep_alive