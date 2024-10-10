import aiohttp
import asyncio
import pytest
from aiohttp import web

@pytest.mark.run_loop
def test_send_recv_text(create_app_and_client):

    @asyncio.coroutine
    def handler(request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)
        msg = yield from ws.receive_str()
        ws.send_str(msg+'/answer')
        yield from ws.close()
        return ws

    app, client = yield from create_app_and_client()
    app.router.add_route('GET', '/', handler)
    resp = yield from client.ws_connect('/')
    resp.send_str('ask')

    msg = yield from resp.receive()
    assert msg.data == 'ask/answer'
    yield from resp.close()