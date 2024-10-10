import collections
import pytest
import re
from unittest import mock
from aiohttp.multidict import CIMultiDict
from aiohttp.web import Request
from aiohttp import signals, web

@pytest.fixture
def buf():
    return bytearray()

@pytest.fixture
def request(buf):
    method = 'GET'
    path = '/'
    headers = CIMultiDict()
    transport = mock.Mock()
    payload = mock.Mock()
    reader = mock.Mock()
    writer = mock.Mock()
    writer.drain.return_value = ()

    def append(data):
        buf.extend(data)
    writer.write.side_effect = append
    app = mock.Mock()
    app._debug = False
    app.on_response_prepare = signals.Signal(app)
    message = RawRequestMessage(method, path, HttpVersion11, headers,
                                False, False)
    req = Request(app, message, payload,
                  transport, reader, writer)
    return req

@pytest.mark.run_loop
def test_HTTPFound(buf, request):
    resp = web.HTTPFound(location='/redirect')
    assert '/redirect' == resp.location
    assert '/redirect' == resp.headers['location']
    yield from resp.prepare(request)
    yield from resp.write_eof()
    txt = buf.decode('utf8')
    assert re.match('HTTP/1.1 302 Found\r\n'
                    'CONTENT-TYPE: text/plain; charset=utf-8\r\n'
                    'CONTENT-LENGTH: 10\r\n'
                    'LOCATION: /redirect\r\n'
                    'CONNECTION: keep-alive\r\n'
                    'DATE: .+\r\n'
                    'SERVER: .+\r\n\r\n'
                    '302: Found', txt)