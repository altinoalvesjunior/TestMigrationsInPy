import aiohttp
import asyncio
import pytest
from aiohttp import web

@pytest.mark.run_loop
def test_close_cancel(create_app_and_client, loop):

    @asyncio.coroutine
    def handler(request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)
        yield from ws.receive_bytes()
        ws.send_str('test')
        yield from asyncio.sleep(10, loop=loop)

    app, client = yield from create_app_and_client()
    app.router.add_route('GET', '/', handler)
    resp = yield from client.ws_connect('/', autoclose=False)
    resp.send_bytes(b'ask')
    text = yield from resp.receive()
    assert text.data == 'test'
    t = loop.create_task(resp.close())
    yield from asyncio.sleep(0.1, loop=loop)
    t.cancel()
    yield from asyncio.sleep(0.1, loop=loop)
    assert resp.closed
    assert resp.exception() is None