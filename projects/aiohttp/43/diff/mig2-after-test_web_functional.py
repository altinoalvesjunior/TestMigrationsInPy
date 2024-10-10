import asyncio
import pytest
from aiohttp import web

@asyncio.coroutine
def test_post_form(loop, test_client):

    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert {'a': '1', 'b': '2'} == data
        return web.Response(body=b'OK')

    app = web.Application(loop=loop)
    app.router.add_post('/', handler)
    client = yield from test_client(app)

    resp = yield from client.post('/', data={'a': 1, 'b': 2})
    assert 200 == resp.status
    txt = yield from resp.text()
    assert 'OK' == txt