import asyncio
from unittest import mock
from aiohttp.multidict import CIMultiDict
from aiohttp.signals import Signal
from aiohttp.web import Application
from aiohttp.web import Request, Response
from aiohttp.protocol import HttpVersion11
from aiohttp.protocol import RawRequestMessage

import pytest

@pytest.fixture
def app(loop):
    return Application(loop=loop)


def make_request(app, method, path, headers=CIMultiDict()):
    message = RawRequestMessage(method, path, HttpVersion11, headers,
                                False, False)
    return request_from_message(message, app)