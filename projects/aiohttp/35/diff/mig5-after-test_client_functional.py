import asyncio
import pytest
import aiohttp
from aiohttp import client, test_utils, web

@pytest.mark.run_loop
def test_HTTP_302_max_redirects(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        return web.Response(text=request.method)
    @asyncio.coroutine
    def redirect(request):
        count = int(request.match_info['count'])
        if count:
            return web.HTTPFound(location='/redirect/{}'.format(count-1))
        else:
            return web.HTTPFound(location='/')

    app, client = yield from create_app_and_client()
    app.router.add_get('/', handler)
    app.router.add_get(r'/redirect/{count:\d+}', redirect)
    resp = yield from client.get('/redirect/5', max_redirects=2)
    assert 302 == resp.status
    assert 2 == len(resp.history)
    resp.close()