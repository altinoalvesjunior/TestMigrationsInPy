import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.asyncio
async def test_session_auth_header_conflict(test_client):
    async def handler(request):
        return web.Response()
    app = web.Application()
    app.router.add_get('/', handler)
    client = await test_client(app, auth=aiohttp.BasicAuth("login", "pass"))
    headers = {'Authorization': "Basic b3RoZXJfbG9naW46cGFzcw=="}
    with pytest.raises(ValueError):
        await client.get('/', headers=headers)