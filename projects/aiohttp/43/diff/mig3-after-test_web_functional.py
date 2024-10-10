import asyncio
import pytest
from aiohttp import web

@asyncio.coroutine
def test_post_text(loop, test_client):

    @asyncio.coroutine
    def handler(request):
        data = yield from request.text()
        assert 'русский' == data
        data2 = yield from request.text()
        assert data == data2
        return web.Response(text=data)

    app = web.Application(loop=loop)
    app.router.add_post('/', handler)
    client = yield from test_client(app)

    resp = yield from client.post('/', data='русский')
    assert 200 == resp.status
    txt = yield from resp.text()
    assert 'русский' == txt