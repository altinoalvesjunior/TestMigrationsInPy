import aiohttp
import asyncio
import unittest
from aiohttp import web

class TestWebSocketClientFunctional(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        if self.handler:
            self.loop.run_until_complete(self.handler.finish_connections())
        self.loop.close()

    @asyncio.coroutine
    def create_server(self, method, path, handler):
        app = web.Application(loop=self.loop)
        app.router.add_route(method, path, handler)
        port = self.find_unused_port()
        self.handler = app.make_handler()
        srv = yield from self.loop.create_server(
            self.handler, '127.0.0.1', port)
        url = "http://127.0.0.1:{}".format(port) + path
        self.addCleanup(srv.close)
        return app, srv, url

    def test_ping_pong(self):

        closed = asyncio.Future(loop=self.loop)

        @asyncio.coroutine
        def handler(request):
            ws = web.WebSocketResponse()
            ws.start(request)

            msg = yield from ws.receive_bytes()
            ws.ping()
            ws.send_bytes(msg+b'/answer')
            try:
                yield from ws.close()
            finally:
                closed.set_result(1)
            return ws

        @asyncio.coroutine
        def go():
            _, _, url = yield from self.create_server('GET', '/', handler)
            resp = yield from aiohttp.ws_connect(url, loop=self.loop)
            resp.ping()
            resp.send_bytes(b'ask')

            msg = yield from resp.receive()
            self.assertEqual(msg.tp, aiohttp.MsgType.binary)
            self.assertEqual(msg.data, b'ask/answer')

            msg = yield from resp.receive()
            self.assertEqual(msg.tp, aiohttp.MsgType.close)

            yield from resp.close()
            yield from closed

        self.loop.run_until_complete(go())

    def find_unused_port(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        port = s.getsockname()[1]
        s.close()
        return port