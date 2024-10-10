import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.run_loop
def test_POST_DATA(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        return web.json_response(dict(data))
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    resp = yield from client.post('/', data={'some': 'data'})
    assert 200 == resp.status
    content = yield from resp.json()
    assert content == {'some': 'data'}
    resp.close()