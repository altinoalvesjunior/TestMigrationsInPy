import asyncio
import pytest
import aiohttp
from aiohttp import client, test_utils, web

@pytest.mark.run_loop
def test_HTTP_307_REDIRECT_POST(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        return web.Response(text=request.method)
    @asyncio.coroutine
    def redirect(request):
        return web.HTTPTemporaryRedirect(location='/')

    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    app.router.add_post('/redirect', redirect)
    resp = yield from client.post('/redirect', data={'some': 'data'})
    assert 200 == resp.status
    assert 1 == len(resp.history)
    txt = yield from resp.text()
    assert txt == 'POST'
    resp.close()