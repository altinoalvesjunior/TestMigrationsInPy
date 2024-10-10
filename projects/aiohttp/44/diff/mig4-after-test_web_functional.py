import asyncio
import pytest
from aiohttp import FormData, web

@asyncio.coroutine
def test_100_continue_for_not_allowed(loop, test_client):
    @asyncio.coroutine
    def handler(request):
        return web.Response()
    app = web.Application(loop=loop)
    app.router.add_post('/', handler)
    client = yield from test_client(app)
    form = FormData()
    form.add_field('name', b'123',
                   content_transfer_encoding='base64')
    resp = yield from client.get('/', data=form, expect100=True)
    assert 405 == resp.status