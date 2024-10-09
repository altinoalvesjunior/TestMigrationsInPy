import asyncio
import pytest
import unittest
from unittest import mock
from aiohttp.signals import Signal
from aiohttp.web import Request
from aiohttp.multidict import MultiDict, CIMultiDict
from aiohttp.protocol import HttpVersion
from aiohttp.protocol import RawRequestMessage

def test_content_length(make_request):
    req = make_request('Get', '/',
                       CIMultiDict([('CONTENT-LENGTH', '123')]))
    assert 123 == req.content_length