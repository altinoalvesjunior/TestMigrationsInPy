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
        
def test_host_port_default_http(make_request):
    req = make_request('get', 'http://python.org/')
    assert req.host == 'python.org'
    assert req.port == 80
    assert not req.ssl
    
def test_host_port_default_https(make_request):
    req = make_request('get', 'https://python.org/')
    assert req.host == 'python.org'
    assert req.port == 443
    assert req.ssl

def test_host_port_nondefault_http(make_request):
    req = make_request('get', 'http://python.org:960/')
    assert req.host == 'python.org'
    assert req.port == 960
    assert not req.ssl