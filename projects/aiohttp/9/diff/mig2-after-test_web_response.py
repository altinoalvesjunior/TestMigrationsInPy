import asyncio
import pytest
from unittest import mock
from aiohttp import hdrs, signals
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
async def test_force_compression_false_backwards_compat():
    req = make_request('GET', '/')
    resp = StreamResponse()

    assert not resp.compression
    resp.enable_compression(force=False)
    assert resp.compression

    with mock.patch('aiohttp.web_reqrep.ResponseImpl') as ResponseImpl:
        msg = await resp.prepare(req)
    assert not msg.add_compression_filter.called