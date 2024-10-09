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

def test_query_bytes_param(make_request):
    for meth in ClientRequest.ALL_METHODS:
        req = make_request(meth, 'http://python.org', params=b'test=foo')
        assert req.path == '/?test=foo'