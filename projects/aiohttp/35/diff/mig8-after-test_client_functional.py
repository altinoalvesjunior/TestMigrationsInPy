import asyncio
import pytest
import aiohttp
from aiohttp import client, test_utils, web

@pytest.mark.run_loop
def test_HTTP_200_GET_WITH_MIXED_PARAMS(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        return web.Response(text='&'.join(
            k+'='+v for k, v in request.GET.items()))

    app, client = yield from create_app_and_client()
    app.router.add_get('/', handler)
    resp = yield from client.get('/?test=true', params={'q': 'test'})
    assert 200 == resp.status
    txt = yield from resp.text()
    assert txt == 'test=true&q=test'
    resp.close()