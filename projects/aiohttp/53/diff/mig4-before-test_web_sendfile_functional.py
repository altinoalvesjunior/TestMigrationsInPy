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

    def test_static_file_huge(self):
        @asyncio.coroutine
        def go(dirname, filename):
            app, _, url = yield from self.create_server(
                'GET', '/static/' + filename
            )
            app.router.add_static('/static', dirname)
            resp = yield from request('GET', url, loop=self.loop)
            self.assertEqual(200, resp.status)
            ct = resp.headers['CONTENT-TYPE']
            self.assertEqual('application/octet-stream', ct)
            self.assertIsNone(resp.headers.get('CONTENT-ENCODING'))
            self.assertEqual(int(resp.headers.get('CONTENT-LENGTH')),
                             file_st.st_size)
            f = open(fname, 'rb')
            off = 0
            cnt = 0
            while off < file_st.st_size:
                chunk = yield from resp.content.readany()
                expected = f.read(len(chunk))
                self.assertEqual(chunk, expected)
                off += len(chunk)
                cnt += 1
            f.close()
            resp.close()
        here = os.path.dirname(__file__)
        filename = 'huge_data.unknown_mime_type'
        # fill 100MB file
        fname = os.path.join(here, filename)
        with open(fname, 'w') as f:
            for i in range(1024*20):
                f.write(chr(i % 64 + 0x20) * 1024)
        self.addCleanup(os.unlink, fname)
        file_st = os.stat(fname)
        self.loop.run_until_complete(go(here, filename))