import asyncio
import gc
import os
import unittest

import aiohttp
from aiohttp import log, request, web
from aiohttp.test_utils import unused_port

try:
    import ssl
except:
    ssl = False

class StaticFileMixin(unittest.TestCase):

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

        app.router.add_static = self.patch_sendfile(app.router.add_static)

        return app, srv, url

    def test_static_file(self):
        @asyncio.coroutine
        def go(dirname, filename):
            app, _, url = yield from self.create_server(
                'GET', '/static/' + filename
            )
            app.router.add_static('/static', dirname)
            resp = yield from request('GET', url, loop=self.loop)
            self.assertEqual(200, resp.status)
            txt = yield from resp.text()
            self.assertEqual('file content', txt.rstrip())
            ct = resp.headers['CONTENT-TYPE']
            self.assertEqual('application/octet-stream', ct)
            self.assertEqual(resp.headers.get('CONTENT-ENCODING'), None)
            resp.close()
            resp = yield from request('GET', url + 'fake', loop=self.loop)
            self.assertEqual(404, resp.status)
            resp.close()
            resp = yield from request('GET', url + 'x' * 500, loop=self.loop)
            self.assertEqual(404, resp.status)
            resp.close()
            resp = yield from request('GET', url + '/../../', loop=self.loop)
            self.assertEqual(404, resp.status)
            resp.close()
        here = os.path.dirname(__file__)
        filename = 'data.unknown_mime_type'
        self.loop.run_until_complete(go(here, filename))