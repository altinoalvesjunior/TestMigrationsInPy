import asyncio
import pytest
from unittest import mock
from aiohttp import helpers, MsgType, errors
from aiohttp.web import WebSocketResponse
from aiohttp.test_utils import make_mocked_request, make_mocked_coro

@pytest.fixture
def loop():
    return asyncio.new_event_loop()

@pytest.fixture
def make_request(app, writer, reader):
    def maker(method, path, headers=None, protocols=False):
        if headers is None:
            headers = {'HOST': 'server.example.com',
                       'UPGRADE': 'websocket',
                       'CONNECTION': 'Upgrade',
                       'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==',
                       'ORIGIN': 'http://example.com',
                       'SEC-WEBSOCKET-VERSION': '13'}
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'

        return make_mocked_request(method, path, headers,
                                   app=app, writer=writer, reader=reader)

    return maker

def test_start_twice_idempotent(make_request):
    req = make_request('GET', '/')
    ws = WebSocketResponse()
    with pytest.warns(DeprecationWarning):
        impl1 = ws.start(req)
        impl2 = ws.start(req)
        assert impl1 is impl2