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

def test_add_signal_handler_not_a_callable(loop, app):
    callback = True
    app.on_response_prepare.append(callback)
    with pytest.raises(TypeError):
        app.on_response_prepare(None, None)