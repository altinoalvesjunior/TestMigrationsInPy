import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.run_loop
def test_POST_FILES_STR(create_app_and_client, fname):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        with fname.open() as f:
            content1 = f.read()
        content2 = data['some']
        assert content1 == content2
        return web.HTTPOk()
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    with fname.open() as f:
        resp = yield from client.post('/', data={'some': f.read()})
        assert 200 == resp.status
        resp.close()