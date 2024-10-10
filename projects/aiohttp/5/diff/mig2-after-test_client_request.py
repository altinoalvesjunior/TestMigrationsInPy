import asyncio
import gc
import unittest
import unittest.mock

import inspect
import io
import urllib.parse
import os.path

from http.cookies import SimpleCookie

import pytest
import aiohttp
from aiohttp.client_reqrep import ClientRequest, ClientResponse
from aiohttp.multidict import upstr, CIMultiDict, CIMultiDictProxy
from aiohttp import BaseConnector


@pytest.yield_fixture
def make_request(loop):
    request = None
    def maker(*args, **kwargs):
        nonlocal request
        request = ClientRequest(*args, loop=loop, **kwargs)
        return request
    yield maker
    if request is not None:
        loop.run_until_complete(request.close())
        
def test_version_1_0(make_request):
    req = make_request('get', 'http://python.org/', version='1.0')
    assert req.version == (1, 0)
