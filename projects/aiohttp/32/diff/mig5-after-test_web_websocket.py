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

@pytest.mark.run_loop
def test_multiple_receive_on_close_connection(make_request):
    req = make_request('GET', '/')
    ws = WebSocketResponse()
    yield from ws.prepare(req)
    yield from ws.close()

    yield from ws.receive()
    yield from ws.receive()
    yield from ws.receive()
    yield from ws.receive()

    with pytest.raises(RuntimeError):
        yield from ws.receive()