import asyncio
import unittest
import aiohttp
from aiohttp import client, test_utils, web
from aiohttp.test_utils import run_briefly, unused_port

class TestHttpClientFunctional(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        test_utils.run_briefly(self.loop)
        self.loop.close()
        gc.collect()

    def test_server_close_keepalive_connection(self):
        class Proto(asyncio.Protocol):
            def connection_made(self, transport):
                self.transp = transport
                self.data = b''
            def data_received(self, data):
                self.data += data
                if data.endswith(b'\r\n\r\n'):
                    self.transp.write(
                        b'HTTP/1.1 200 OK\r\n'
                        b'CONTENT-LENGTH: 2\r\n'
                        b'CONNECTION: close\r\n'
                        b'\r\n'
                        b'ok')
                    self.transp.close()
            def connection_lost(self, exc):
                self.transp = None
        async def go():
            server = await self.loop.create_server(
                Proto, '127.0.0.1', unused_port())
            addr = server.sockets[0].getsockname()
            connector = aiohttp.TCPConnector(loop=self.loop, limit=1)
            session = client.ClientSession(loop=self.loop, connector=connector)
            url = 'http://{}:{}/'.format(*addr)
            for i in range(2):
                r = await session.request('GET', url)
                await r.read()
                self.assertEqual(0, len(connector._conns))
            await session.close()
            connector.close()
            server.close()
            await server.wait_closed()
        self.loop.run_until_complete(go())