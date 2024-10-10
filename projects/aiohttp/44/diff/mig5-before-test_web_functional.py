import asyncio
import gc
import unittest
from aiohttp import ClientSession, FormData, log, request, web
from aiohttp.protocol import HttpVersion, HttpVersion11
from aiohttp.test_utils import unused_port

class TestWebFunctional(unittest.TestCase):

    def setUp(self):
        self.handler = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        if self.handler:
            self.loop.run_until_complete(self.handler.finish_connections())
        self.loop.stop()
        self.loop.run_forever()
        self.loop.close()
        gc.collect()

    @asyncio.coroutine
    def create_server(self, method, path, handler=None, ssl_ctx=None,
                      logger=log.server_logger, handler_kwargs=None):
        app = web.Application(
            loop=self.loop)
        if handler:
            app.router.add_route(method, path, handler)
        port = unused_port()
        self.handler = app.make_handler(
            keep_alive_on=False,
            access_log=log.access_logger,
            logger=logger,
            **(handler_kwargs or {}))
        srv = yield from self.loop.create_server(
            self.handler, '127.0.0.1', port, ssl=ssl_ctx)
        protocol = "https" if ssl_ctx else "http"
        url = "{}://127.0.0.1:{}".format(protocol, port) + path
        self.addCleanup(srv.close)
        return app, srv, url

    def test_http11_keep_alive_default(self):
        @asyncio.coroutine
        def handler(request):
            yield from request.read()
            return web.Response(body=b'OK')
        @asyncio.coroutine
        def go():
            _, _, url = yield from self.create_server('GET', '/', handler)
            resp = yield from request('GET', url, loop=self.loop,
                                      version=HttpVersion11)
            self.assertNotIn('CONNECTION', resp.headers)
            resp.close()
        self.loop.run_until_complete(go())