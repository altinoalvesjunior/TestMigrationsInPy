import asyncio
import os
import unittest
import aiohttp
from aiohttp import web, client
from aiohttp.test_utils import unused_port

class TestHttpClientConnector(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.stop()
        self.loop.run_forever()
        self.loop.close()

    async def create_server(self, method, path, handler):
        app = web.Application()
        app.router.add_route(method, path, handler)
        port = unused_port()
        self.handler = app.make_handler(loop=self.loop, tcp_keepalive=False)
        srv = await self.loop.create_server(
            self.handler, '127.0.0.1', port)
        url = "http://127.0.0.1:{}".format(port) + path
        return app, srv, url

    def test_tcp_connector_uses_provided_local_addr(self):
        async def handler(request):
            return web.Response()

        app, srv, url = self.loop.run_until_complete(
            self.create_server('get', '/', handler)
        )

        port = unused_port()
        conn = aiohttp.TCPConnector(loop=self.loop,
                                    local_addr=('127.0.0.1', port))

        session = aiohttp.ClientSession(connector=conn)

        r = self.loop.run_until_complete(
            session.request('get', url)
        )

        r.release()
        first_conn = next(iter(conn._conns.values()))[0][0]
        self.assertEqual(
            first_conn.transport._sock.getsockname(), ('127.0.0.1', port))
        r.close()
        self.loop.run_until_complete(session.close())
        conn.close()