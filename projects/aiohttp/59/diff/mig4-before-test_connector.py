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

    async def create_unix_server(self, method, path, handler):
        tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmpdir)
        app = web.Application()
        app.router.add_route(method, path, handler)
        self.handler = app.make_handler(
            loop=self.loop, tcp_keepalive=False, access_log=None)
        sock_path = os.path.join(tmpdir, 'socket.sock')
        srv = await self.loop.create_unix_server(
            self.handler, sock_path)
        url = "http://127.0.0.1" + path
        return app, srv, url, sock_path

    @unittest.skipUnless(hasattr(socket, 'AF_UNIX'), 'requires unix')
    def test_unix_connector(self):
        async def handler(request):
            return web.Response()

        app, srv, url, sock_path = self.loop.run_until_complete(
            self.create_unix_server('get', '/', handler))

        connector = aiohttp.UnixConnector(sock_path, loop=self.loop)
        self.assertEqual(sock_path, connector.path)

        session = client.ClientSession(
            connector=connector, loop=self.loop)
        r = self.loop.run_until_complete(
            session.request('get', url))
        self.assertEqual(r.status, 200)
        r.close()
        self.loop.run_until_complete(session.close())