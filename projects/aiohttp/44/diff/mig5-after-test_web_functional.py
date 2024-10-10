import asyncio
import pytest
from aiohttp import web
from aiohttp.protocol import HttpVersion11

@asyncio.coroutine
def test_http11_keep_alive_default(loop, test_client):
    @asyncio.coroutine
    def handler(request):
        yield from request.read()
        return web.Response(body=b'OK')
    app = web.Application(loop=loop)
    app.router.add_get('/', handler)
    client = yield from test_client(app)
    resp = yield from client.get('/', version=HttpVersion11)
    assert 200 == resp.status
    assert 'Connection' not in resp.headers