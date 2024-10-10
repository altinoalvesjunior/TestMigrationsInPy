import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.asyncio
async def test_dont_close_explicit_connector(test_client):
    async def handler(request):
        return web.Response()
    app = web.Application()
    app.router.add_get('/', handler)
    client = await test_client(app)
    r = await client.get('/')
    await r.read()
    assert 1 == len(client.session.connector._conns)