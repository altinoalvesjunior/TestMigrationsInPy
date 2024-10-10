import asyncio
import os
import ssl
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

    async def create_server(self, method, path, handler, ssl_context=None):
        app = web.Application()
        app.router.add_route(method, path, handler)
        port = unused_port()
        self.handler = app.make_handler(loop=self.loop, tcp_keepalive=False)
        srv = await self.loop.create_server(
            self.handler, '127.0.0.1', port, ssl=ssl_context)
        scheme = 's' if ssl_context is not None else ''
        url = "http{}://127.0.0.1:{}".format(scheme, port) + path
        return app, srv, url

    def test_tcp_connector_do_not_raise_connector_ssl_error(self):
        async def handler(request):
            return web.Response()

        here = os.path.join(os.path.dirname(__file__), '..', 'tests')
        keyfile = os.path.join(here, 'sample.key')
        certfile = os.path.join(here, 'sample.crt')
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslcontext.load_cert_chain(certfile, keyfile)
        app, srv, url = self.loop.run_until_complete(
            self.create_server('get', '/', handler, ssl_context=sslcontext)
        )

        port = unused_port()
        conn = aiohttp.TCPConnector(loop=self.loop,
                                    local_addr=('127.0.0.1', port))

        session = aiohttp.ClientSession(connector=conn)

        r = self.loop.run_until_complete(
            session.request('get', url, ssl=sslcontext))

        r.release()
        first_conn = next(iter(conn._conns.values()))[0][0]

        try:
            _sslcontext = first_conn.transport._ssl_protocol._sslcontext
        except AttributeError:
            _sslcontext = first_conn.transport._sslcontext

        self.assertIs(_sslcontext, sslcontext)
        r.close()

        self.loop.run_until_complete(session.close())
        conn.close()