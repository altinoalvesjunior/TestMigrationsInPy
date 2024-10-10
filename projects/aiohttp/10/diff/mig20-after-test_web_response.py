import asyncio
import pytest
from aiohttp import signals
from aiohttp.web import ContentCoding, Request, StreamResponse, Response
from aiohttp.protocol import HttpVersion, HttpVersion10
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
async def test_chunked_encoding_forbidden_for_http_10():
    req = make_request('GET', '/', version=HttpVersion10)
    resp = StreamResponse()
    resp.enable_chunked_encoding()

    with pytest.raises(RuntimeError, match="Using chunked encoding is forbidden for HTTP/1.0"):
        await resp.prepare(req)