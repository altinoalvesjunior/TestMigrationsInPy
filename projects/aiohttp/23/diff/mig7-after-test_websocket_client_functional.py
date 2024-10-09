import aiohttp
import asyncio
import pytest
from aiohttp import web

@pytest.mark.run_loop
def test_close_manual(create_app_and_client, loop):

    closed = asyncio.Future(loop=loop)

    @asyncio.coroutine
    def handler(request):
        ws = web.WebSocketResponse()
        yield from ws.prepare(request)

        yield from ws.receive_bytes()
        ws.send_str('test')

        try:
            yield from ws.close()
        finally:
            closed.set_result(1)
        return ws

    app, client = yield from create_app_and_client()
    app.router.add_route('GET', '/', handler)
    resp = yield from client.ws_connect('/', autoclose=False)
    resp.send_bytes(b'ask')

    msg = yield from resp.receive()
    assert msg.data == 'test'

    msg = yield from resp.receive()
    assert msg.tp == aiohttp.MsgType.close
    assert msg.data == 1000
    assert msg.extra == ''
    assert not resp.closed

    yield from resp.close()
    yield from closed
    assert resp.closed