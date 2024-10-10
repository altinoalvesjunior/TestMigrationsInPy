import asyncio
import pytest
from aiohttp import web
from aiohttp.protocol import HttpVersion11

@asyncio.coroutine
def test_head_returns_empty_body(loop, test_client):

    @asyncio.coroutine
    def handler(request):
        return web.Response(body=b'test')
    app = web.Application(loop=loop)
    app.router.add_head('/', handler)
    client = yield from test_client(app)
    resp = yield from client.head('/', version=HttpVersion11)
    assert 200 == resp.status
    txt = yield from resp.text()
    assert '' == txt