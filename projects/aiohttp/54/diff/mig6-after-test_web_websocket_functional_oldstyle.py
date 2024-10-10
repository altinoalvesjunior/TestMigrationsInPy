import asyncio
import base64
import hashlib
import os

import pytest
import aiohttp
from aiohttp import helpers, web


WS_KEY = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

@pytest.fixture
@asyncio.coroutine
def create_server(loop, test_server):
    @asyncio.coroutine
    def maker(method, path, handler):
        app = web.Application(loop=loop)
        app.router.add_route(method, path, handler)
        server = yield from test_server(app)
        url = str(server.make_url(path))
        return app, server, url
    return maker

@pytest.fixture
@asyncio.coroutine
def connect_ws(loop, test_client):
    @asyncio.coroutine
    def connector(url, protocol=None):
        sec_key = base64.b64encode(os.urandom(16))
        conn = aiohttp.TCPConnector(loop=loop)
        headers = {
            'UPGRADE': 'WebSocket',
            'CONNECTION': 'Upgrade',
            'SEC-WEBSOCKET-VERSION': '13',
            'SEC-WEBSOCKET-KEY': sec_key.decode(),
        }
        if protocol:
            headers['SEC-WEBSOCKET-PROTOCOL'] = protocol
        client = yield from test_client(web.Application(loop=loop))
        response = yield from client.get(url, headers=headers)
        assert response.status == 101
        assert response.headers.get('upgrade', '').lower() == 'websocket'
        assert response.headers.get('connection', '').lower() == 'upgrade'
        key = response.headers.get('sec-websocket-accept', '').encode()
        match = base64.b64encode(hashlib.sha1(sec_key + WS_KEY).digest())
        assert key == match
        connection = response.connection
        reader = connection.reader.set_parser(WebSocketParser)
        writer = WebSocketWriter(connection.writer)
        return response, reader, writer
    return connector

@asyncio.coroutine
def test_receive_msg(create_server, connect_ws, loop):
    @asyncio.coroutine
    def handler(request):
        ws =         ws = web.WebSocketResponse()
        yield from ws.prepare(request)
        with pytest.warns(DeprecationWarning):
            msg = yield from ws.receive_msg()
            assert msg.data == b'data'
        yield from ws.close()
        return ws
    app, server, url = yield from create_server('GET', '/', handler)
    client = yield from connect_ws(url)
    client.send_bytes(b'data')
    yield from client.close()