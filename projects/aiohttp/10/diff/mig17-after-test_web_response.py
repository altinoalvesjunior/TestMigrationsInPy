import asyncio
import pytest
from unittest import mock
from aiohttp import signals
from aiohttp.web import ContentCoding, Request, StreamResponse, Response
from aiohttp.protocol import HttpVersion, HttpVersion11, HttpVersion10
from aiohttp.protocol import RawRequestMessage
from aiohttp.multidict import CIMultiDict

def make_request(method, path, headers=CIMultiDict(),
                 version=HttpVersion11, **kwargs):
    message = RawRequestMessage(method, path, version, headers,
                                False, False)
    return request_from_message(message, **kwargs)

def request_from_message(message, **kwargs):
    app = mock.Mock()
    app._debug = False
    app.on_response_prepare = signals.Signal(app)
    payload = mock.Mock()
    transport = mock.Mock()
    reader = mock.Mock()
    writer = kwargs.get('writer') or mock.Mock()
    req = Request(app, message, payload,
                  transport, reader, writer)
    return req

@pytest.mark.asyncio
async def test_start():
    req = make_request('GET', '/')
    resp = StreamResponse()
    assert resp.keep_alive is None

    with mock.patch('aiohttp.web_reqrep.ResponseImpl'):
        msg = await resp.prepare(req)

        assert msg.send_headers.called
        msg2 = await resp.prepare(req)
        assert msg is msg2

        assert resp.keep_alive

    req2 = make_request('GET', '/')
    with pytest.raises(RuntimeError):
        await resp.prepare(req2)