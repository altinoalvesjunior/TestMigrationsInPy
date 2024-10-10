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
def test_close_exc(make_request, reader, loop):
    req = make_request('GET', '/')
    ws = WebSocketResponse()
    yield from ws.prepare(req)
    exc = ValueError()
    reader.read.return_value = helpers.create_future(loop)
    reader.read.return_value.set_exception(exc)
    yield from ws.close()
    assert ws.closed
    assert ws.exception() is exc
    ws._closed = False
    reader.read.return_value = helpers.create_future(loop)
    reader.read.return_value.set_exception(asyncio.CancelledError())
    with pytest.raises(asyncio.CancelledError):
        yield from ws.close()
    assert ws.close_code == 1006