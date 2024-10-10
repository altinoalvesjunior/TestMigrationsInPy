import asyncio
import gc
import os
import unittest

import aiohttp
from aiohttp import log, request, web
from aiohttp.test_utils import unused_port

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

    def test_static_file_directory_traversal_attack(self):
        @asyncio.coroutine
        def go(dirname, relpath):
            self.assertTrue(os.path.isfile(os.path.join(dirname, relpath)))
            app, _, url = yield from self.create_server('GET', '/static/')
            app.router.add_static('/static', dirname)
            url_relpath = url + relpath
            resp = yield from request('GET', url_relpath, loop=self.loop)
            self.assertEqual(404, resp.status)
            resp.close()
            url_relpath2 = url + 'dir/../' + relpath
            resp = yield from request('GET', url_relpath2, loop=self.loop)
            self.assertEqual(404, resp.status)
            resp.close()
            url_abspath = \
                url + os.path.abspath(os.path.join(dirname, relpath))
            resp = yield from request('GET', url_abspath, loop=self.loop)
            self.assertEqual(404, resp.status)
            resp.close()
        here = os.path.dirname(__file__)
        relpath = '../README.rst'
        self.loop.run_until_complete(go(here, relpath))