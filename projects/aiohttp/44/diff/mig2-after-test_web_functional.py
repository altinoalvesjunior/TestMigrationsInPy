import asyncio
import pytest
from aiohttp import FormData, web

@asyncio.coroutine
def test_100_continue_custom_response(loop, test_client):
    auth_err = False
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert b'123' == data['name']
        return web.Response()
    @asyncio.coroutine
    def expect_handler(request):
        nonlocal auth_err
        if request.version == HttpVersion11:
            if auth_err:
                return web.HTTPForbidden()
            request.transport.write(b"HTTP/1.1 100 Continue\r\n\r\n")
    form = FormData()
    form.add_field('name', b'123',
                   content_transfer_encoding='base64')
    app = web.Application(loop=loop)
    app.router.add_post('/', handler, expect_handler=expect_handler)
    client = yield from test_client(app)
    resp = yield from client.post('/', data=form, expect100=True)
    assert 200 == resp.status
    auth_err = True
    resp = yield from client.post('/', data=form, expect100=True)
    assert 403 == resp.status