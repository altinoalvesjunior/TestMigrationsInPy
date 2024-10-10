import asyncio
import pytest
from aiohttp import web


@pytest.mark.run_loop
def test_middleware_modifies_response(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        return web.Response(body=b'OK')
    
    @asyncio.coroutine
    def middleware_factory(app, handler):
        def middleware(request):
            resp = yield from handler(request)
            assert 200 == resp.status
            resp.set_status(201)
            resp.text = resp.text + '[MIDDLEWARE]'
            return resp
        return middleware
    
    app, client = yield from create_app_and_client()
    app.middlewares.append(middleware_factory)
    app.router.add_route('GET', '/', handler)
    resp = yield from client.get('/')
    assert 201 == resp.status
    txt = yield from resp.text()
    assert 'OK[MIDDLEWARE]' == txt