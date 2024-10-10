import asyncio
import pytest
from aiohttp import FormData, web

@asyncio.coroutine
def test_100_continue_for_not_found(loop, test_client):
    app = web.Application(loop=loop)
    client = yield from test_client(app)
    form = FormData()
    form.add_field('name', b'123',
                   content_transfer_encoding='base64')
    resp = yield from client.post('/not_found', data=form, expect100=True)
    assert 404 == resp.status