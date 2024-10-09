import asyncio
import pytest
from unittest import mock
from aiohttp import helpers, MsgType, errors
from aiohttp.web import WebSocketResponse, Request
from aiohttp.protocol import RawRequestMessage, HttpVersion11
from aiohttp.test_utils import make_mocked_request, make_mocked_coro
from aiohttp import signals

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
def test_receive_exc_in_reader(make_request, loop, reader):
    req = make_request('GET', '/')
    ws = WebSocketResponse()
    yield from ws.prepare(req)
    exc = ValueError()
    res = helpers.create_future(loop)
    res.set_exception(exc)
    reader.read = make_mocked_coro(res)
    msg = yield from ws.receive()
    assert msg.tp == MsgType.error
    assert msg.data is exc
    assert ws.exception() is exc