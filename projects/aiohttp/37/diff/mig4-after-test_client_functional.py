import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.run_loop
def test_POST_FILES_STR_SIMPLE(create_app_and_client, fname):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.read()
        with fname.open('rb') as f:
            content = f.read()
        assert content == data
        return web.HTTPOk()
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    with fname.open() as f:
        resp = yield from client.post('/', data=f.read())
        assert 200 == resp.status
        resp.close()