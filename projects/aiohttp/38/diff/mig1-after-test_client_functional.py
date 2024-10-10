import asyncio
import pytest
import aiohttp
from aiohttp import client, test_utils, web

@pytest.mark.run_loop
def test_POST_DATA_with_charset(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        return web.HTTPOk(text=data['name'])
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    form = aiohttp.FormData()
    form.add_field('name', 'текст', content_type='text/plain; charset=koi8-r')
    resp = yield from client.post('/', data=form)
    assert 200 == resp.status
    content = yield from resp.text()
    assert content == 'текст'
    resp.close()