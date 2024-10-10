import asyncio
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.run_loop
def test_POST_FILES(create_app_and_client, fname):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert data['some'].filename == fname.name
        with fname.open('rb') as f:
            content1 = f.read()
        content2 = data['some'].file.read()
        assert content1 == content2
        assert data['test'].file.read() == b'data'
        return web.HTTPOk()
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    with fname.open() as f:
        resp = yield from client.post('/', data={'some': f, 'test': b'data'},
                                      chunked=1024,
                                      headers={'Transfer-Encoding': 'chunked'})
        assert 200 == resp.status
        resp.close()