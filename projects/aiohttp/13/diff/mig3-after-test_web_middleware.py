import asyncio
import pytest
from aiohttp import web

@pytest.mark.run_loop
def test_middleware_chain(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        return web.Response(text='OK')

    def make_factory(num):
        @asyncio.coroutine
        def factory(app, handler):
            def middleware(request):
                resp = yield from handler(request)
                resp.text = resp.text + '[{}]'.format(num)
                return resp
            return middleware
        return factory

    app, client = yield from create_app_and_client()
    app.middlewares.append(make_factory(1))
    app.middlewares.append(make_factory(2))
    app.router.add_route('GET', '/', handler)
    resp = yield from client.get('/')
    assert 200 == resp.status
    txt = yield from resp.text()
    assert 'OK[2][1]' == txt