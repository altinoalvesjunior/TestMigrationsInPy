import aiohttp
import asyncio
import pytest
from aiohttp import web

@pytest.mark.run_loop
def test_close(create_app_and_client):

    @asyncio.coroutine
    def handler(request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)

        yield from ws.receive_bytes()
        ws.send_str('test')

        yield from ws.receive()
        return ws

    app, client = yield from create_app_and_client()
    app.router.add_route('GET', '/', handler)
    resp = yield from client.ws_connect('/')

    resp.send_bytes(b'ask')

    closed = yield from resp.close()
    assert closed
    assert resp.closed
    assert resp.close_code == 1000

    msg = yield from resp.receive()
    assert msg.tp == aiohttp.MsgType.closed