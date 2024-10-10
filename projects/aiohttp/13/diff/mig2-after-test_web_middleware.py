import asyncio
import pytest
from aiohttp import web

@pytest.mark.run_loop
def test_middleware_handles_exception(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        raise RuntimeError('Error text')

    @asyncio.coroutine
    def middleware_factory(app, handler):
        @asyncio.coroutine
        def middleware(request):
            with pytest.raises(RuntimeError) as ctx:
                yield from handler(request)
            return web.Response(status=501,
                                text=str(ctx.value) + '[MIDDLEWARE]')
        return middleware

    app, client = yield from create_app_and_client()
    app.middlewares.append(middleware_factory)
    app.router.add_route('GET', '/', handler)
    resp = yield from client.get('/')
    assert 501 == resp.status
    txt = yield from resp.text()
    assert 'Error text[MIDDLEWARE]' == txt