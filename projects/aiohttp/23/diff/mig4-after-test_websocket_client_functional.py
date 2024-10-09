import aiohttp
import asyncio
import pytest
from aiohttp import web

@pytest.mark.run_loop
def test_ping_pong_manual(create_app_and_client, loop):

    closed = asyncio.Future(loop=loop)

    @asyncio.coroutine
    def handler(request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)
        msg = yield from ws.receive_bytes()
        ws.ping()
        ws.send_bytes(msg+b'/answer')
        try:
            yield from ws.close()
        finally:
            closed.set_result(1)
        return ws

    app, client = yield from create_app_and_client()
    app.router.add_route('GET', '/', handler)
    resp = yield from client.ws_connect('/', autoping=False)

    resp.ping()
    resp.send_bytes(b'ask')

    msg = yield from resp.receive()
    assert msg.tp == aiohttp.MsgType.pong

    msg = yield from resp.receive()
    assert msg.tp == aiohttp.MsgType.ping
    resp.pong()

    msg = yield from resp.receive()
    assert msg.data == b'ask/answer'

    msg = yield from resp.receive()
    assert msg.tp == aiohttp.MsgType.close

    yield from closed