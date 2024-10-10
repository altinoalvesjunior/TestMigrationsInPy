import asyncio
import gc
import os
import unittest

import aiohttp
from aiohttp import log, web
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

    @unittest.skipUnless(ssl, "ssl not supported")
    def test_static_file_ssl(self):
        @asyncio.coroutine
        def go(dirname, filename):
            ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            ssl_ctx.load_cert_chain(
                os.path.join(dirname, 'sample.crt'),
                os.path.join(dirname, 'sample.key')
            )
            app, _, url = yield from self.create_server(
                'GET', '/static/' + filename, ssl_ctx=ssl_ctx
            )
            app.router.add_static('/static', dirname)
            conn = aiohttp.TCPConnector(verify_ssl=False, loop=self.loop)
            session = aiohttp.ClientSession(connector=conn)
            resp = yield from session.request('GET', url)
            self.assertEqual(200, resp.status)
            txt = yield from resp.text()
            self.assertEqual('file content', txt.rstrip())
            ct = resp.headers['CONTENT-TYPE']
            self.assertEqual('application/octet-stream', ct)
            self.assertEqual(resp.headers.get('CONTENT-ENCODING'), None)
            resp.close()
            session.close()
        here = os.path.dirname(__file__)
        filename = 'data.unknown_mime_type'
        self.loop.run_until_complete(go(here, filename))