import asyncio
import pytest
import io
import aiohttp
from aiohttp import client, test_utils, web

@pytest.mark.run_loop
def test_POST_FILES_IO(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert data['some'].filename == fname.name
        with fname.open('rb') as f:
            content1 = f.read()
        content2 = data['some'].file.read()
        assert content1 == content2
        return web.HTTPOk()
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    data = io.BytesIO(b'data')
    resp = yield from client.post('/', data=[data])
    content = yield from resp.json()
    assert 1 == len(content['multipart-data'])
    assert content['multipart-data'][0] ==