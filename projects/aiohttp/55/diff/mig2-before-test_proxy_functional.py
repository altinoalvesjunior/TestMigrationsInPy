import asyncio
import base64
import hashlib
import os
import unittest
import aiohttp
from aiohttp import WSMsgType, helpers, web
from aiohttp._ws_impl import WebSocketParser, WebSocketWriter
from aiohttp.test_utils import unused_port

WS_KEY = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

class TestWebWebSocketFunctional(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    @asyncio.coroutine
    def create_server(self, method, path, handler):
        app = web.Application(loop=self.loop)
        app.router.add_route(method, path, handler)
        port = unused_port()
        srv = yield from self.loop.create_server(
            app.make_handler(), '127.0.0.1', port)
        url = "http://127.0.0.1:{}".format(port) + path
        self.addCleanup(srv.close)
        return app, srv, url

    @asyncio.coroutine
    def connect_ws(self, url, protocol=None):
        sec_key = base64.b64encode(os.urandom(16))
        conn = aiohttp.TCPConnector(loop=self.loop)
        self.addCleanup(conn.close)
        headers = {
            'UPGRADE': 'WebSocket',
            'CONNECTION': 'Upgrade',
            'SEC-WEBSOCKET-VERSION': '13',
            'SEC-WEBSOCKET-KEY': sec_key.decode(),
        }
        if protocol:
            headers['SEC-WEBSOCKET-PROTOCOL'] = protocol
        # send request
        response = yield from aiohttp.request(
            'get', url,
            headers=headers,
            connector=conn,
            loop=self.loop)
        self.addCleanup(response.close)
        self.assertEqual(101, response.status)
        self.assertEqual(response.headers.get('upgrade', '').lower(),
                         'websocket')
        self.assertEqual(response.headers.get('connection', '').lower(),
                         'upgrade')
        key = response.headers.get('sec-websocket-accept', '').encode()
        match = base64.b64encode(hashlib.sha1(sec_key + WS_KEY).digest())
        self.assertEqual(key, match)
        # switch to websocket protocol
        connection = response.connection
        reader = connection.reader.set_parser(WebSocketParser)
        writer = WebSocketWriter(connection.writer)
        return response, reader, writer

    def test_handle_protocol(self):
        closed = helpers.create_future(self.loop)
        @asyncio.coroutine
        def handler(request):
            ws = web.WebSocketResponse(protocols=('foo', 'bar'))
            yield from ws.prepare(request)
            yield from ws.close()
            self.assertEqual('bar', ws.protocol)
            closed.set_result(None)
            return ws
        @asyncio.coroutine
        def go():
            _, _, url = yield from self.create_server('GET', '/', handler)
            resp, _, writer = yield from self.connect_ws(url, 'eggs, bar')
            writer.close()
            yield from closed
            resp.close()
        self.loop.run_until_complete(go())