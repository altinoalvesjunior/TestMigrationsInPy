import aiohttp
import asyncio
import pytest
from aiohttp import web

@pytest.mark.run_loop
def test_close_timeout(create_app_and_client, loop):

    @asyncio.coroutine
    def handler(request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)
        yield from ws.receive_bytes()
        ws.send_str('test')
        yield from asyncio.sleep(10, loop=loop)

    app, client = yield from create_app_and_client()
    app.router.add_route('GET', '/', handler)
    resp = yield from client.ws_connect('/', timeout=0.2, autoclose=False)

    resp.send_bytes(b'ask')

    msg = yield from resp.receive()
    assert msg.data == 'test'
    assert msg.tp == aiohttp.MsgType.text

    msg = yield from resp.close()
    assert resp.closed
    assert isinstance(resp.exception(), asyncio.TimeoutError)