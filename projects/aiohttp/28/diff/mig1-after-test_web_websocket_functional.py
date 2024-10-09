import asyncio
import pytest
import aiohttp
from aiohttp import web
from aiohttp import helpers

@pytest.mark.run_loop
def test_send_recv_bytes(create_app_and_client, loop):
    closed = helpers.create_future(loop)
    @asyncio.coroutine
    def handler(request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)
        msg = yield from ws.receive_bytes()
        ws.send_bytes(msg+b'/answer')
        yield from ws.close()
        closed.set_result(1)
        return ws
    app, client = yield from create_app_and_client()
    app.router.add_route('GET', '/', handler)
    ws = yield from client.ws_connect('/')
    ws.send_bytes(b'ask')
    msg = yield from ws.receive()
    assert msg.tp == aiohttp.MsgType.binary
    assert b'ask/answer' == msg.data
    msg = yield from ws.receive()
    assert msg.tp == aiohttp.MsgType.close
    assert msg.data == 1000
    assert msg.extra == ''
    assert ws.closed
    assert ws.close_code == 1000
    yield from closed