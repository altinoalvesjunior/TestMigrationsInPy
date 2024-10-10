import asyncio
import pytest
import aiohttp
from aiohttp import client, test_utils, web

@pytest.mark.run_loop
def test_HTTP_302_REDIRECT_POST(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        return web.Response(text=request.method)
    @asyncio.coroutine
    def redirect(request):
        return web.HTTPFound(location='/')

    app, client = yield from create_app_and_client()
    app.router.add_get('/', handler)
    app.router.add_post('/redirect', redirect)
    resp = yield from client.post('/redirect')
    assert 200 == resp.status
    assert 1 == len(resp.history)
    txt = yield from resp.text()
    assert txt == 'GET'
    resp.close()