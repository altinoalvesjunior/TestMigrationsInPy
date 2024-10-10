import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.asyncio
async def test_server_close_keepalive_connection(loop):
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
    server = await loop.create_server(
        Proto, '127.0.0.1', unused_port())
    addr = server.sockets[0].getsockname()
    connector = aiohttp.TCPConnector(loop=loop, limit=1)
    session = aiohttp.ClientSession(loop=loop, connector=connector)
    url = 'http://{}:{}/'.format(*addr)
    for i in range(2):
        r = await session.request('GET', url)
        await r.read()
        assert 0 == len(connector._conns)
    await session.close()
    connector.close()
    server.close()
    await server.wait_closed()