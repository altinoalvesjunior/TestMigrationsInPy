import asyncio
import pytest
from aiohttp import FormData, web
from aiohttp.protocol import HttpVersion11

@asyncio.coroutine
def test_100_continue_custom(loop, test_client):
    expect_received = False
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert b'123' == data['name']
        return web.Response()
    @asyncio.coroutine
    def expect_handler(request):
        nonlocal expect_received
        expect_received = True
        if request.version == HttpVersion11:
            request.transport.write(b"HTTP/1.1 100 Continue\r\n\r\n")
    form = FormData()
    form.add_field('name', b'123',
                   content_transfer_encoding='base64')
    app = web.Application(loop=loop)
    app.router.add_post('/', handler, expect_handler=expect_handler)
    client = yield from test_client(app)
    resp = yield from client.post('/', data=form, expect100=True)
    assert 200 == resp.status
    assert expect_received