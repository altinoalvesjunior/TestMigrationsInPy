import asyncio
import pytest
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

def test_non_keepalive_on_http10(make_request):
    req = make_request('GET', '/', version=HttpVersion(1, 0))
    assert not req.keep_alive