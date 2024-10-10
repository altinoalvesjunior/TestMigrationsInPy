import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.asyncio
async def test_session_auth_override(test_client):
    async def handler(request):
        return web.json_response({'headers': dict(request.headers)})
    app = web.Application()
    app.router.add_get('/', handler)
    client = await test_client(app, auth=aiohttp.BasicAuth("login", "pass"))
    r = await client.get('/', auth=aiohttp.BasicAuth("other_login", "pass"))
    assert r.status == 200
    content = await r.json()
    val = content['headers']["Authorization"]
    assert val == "Basic b3RoZXJfbG9naW46cGFzcw=="