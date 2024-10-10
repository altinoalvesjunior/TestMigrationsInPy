import asyncio
import pytest
import aiohttp
from aiohttp import client, test_utils, web

@pytest.mark.run_loop
def test_POST_DATA_with_content_transfer_encoding(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert data['name'] == b'123'
        return web.HTTPOk()
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    form = aiohttp.FormData()
    form.add_field('name', b'123', content_transfer_encoding='base64')
    resp = yield from client.post('/', data=form)
    assert 200 == resp.status
    resp.close()