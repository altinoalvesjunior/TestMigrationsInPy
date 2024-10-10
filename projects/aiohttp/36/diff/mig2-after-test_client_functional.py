import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.run_loop
def test_POST_DATA_with_explicit_formdata(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        return web.json_response(dict(data))
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    form = aiohttp.FormData()
    form.add_field('name', 'text')
    resp = yield from client.post('/', data=form)
    assert 200 == resp.status
    content = yield from resp.json()
    assert content == {'name': 'text'}
    resp.close()