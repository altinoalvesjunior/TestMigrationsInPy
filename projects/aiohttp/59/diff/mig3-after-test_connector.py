import asyncio
import os
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.asyncio
async def test_tcp_connector_uses_provided_local_addr(aiohttp_server):
    async def handler(request):
        return web.Response()

    app = web.Application()
    app.router.add_get('/', handler)
    srv = await aiohttp_server(app)

    port = unused_port()
    conn = aiohttp.TCPConnector(local_addr=('127.0.0.1', port))

    session = aiohttp.ClientSession(connector=conn)
    url = srv.make_url('/')

    r = await session.get(url)
    r.release()

    first_conn = next(iter(conn._conns.values()))[0][0]
    assert first_conn.transport.get_extra_info(
        'sockname') == ('127.0.0.1', port)
    r.close()
    await session.close()
    conn.close()