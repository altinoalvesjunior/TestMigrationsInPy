import asyncio
import pytest
import aiohttp
from aiohttp import web
from aiohttp import helpers

@pytest.mark.run_loop
def test_send_recv_text(create_app_and_client, loop):
    closed = helpers.create_future(loop)
    @asyncio.coroutine
    def handler(request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)
        msg = yield from ws.receive_str()
        ws.send_str(msg+'/answer')
        yield from ws.close()
        closed.set_result(1)
        return ws
    app, client = yield from create_app_and_client()
    app.router.add_route('GET', '/', handler)
    ws = yield from client.ws_connect('/')
    ws.send_str('ask')
    msg = yield from ws.receive()
    assert msg.tp == aiohttp.MsgType.text
    assert 'ask/answer' == msg.data
    msg = yield from ws.receive()
    assert msg.tp == aiohttp.MsgType.close
    assert msg.data == 1000
    assert msg.extra == ''
    assert ws.closed
    assert ws.close_code == 1000
    yield from closed