import asyncio
import os
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.skipif(not hasattr(socket, 'AF_UNIX'),
                    reason='requires UNIX sockets')
@pytest.mark.asyncio
async def test_unix_connector(unix_server, unix_sockname):
    async def handler(request):
        return web.Response()

    app = web.Application()
    app.router.add_get('/', handler)
    await unix_server(app)
    url = "http://127.0.0.1/"
    connector = aiohttp.UnixConnector(unix_sockname)
    assert unix_sockname == connector.path
    session = client.ClientSession(connector=connector)
    r = await session.get(url)
    assert r.status == 200
    r.close()
    await session.close()