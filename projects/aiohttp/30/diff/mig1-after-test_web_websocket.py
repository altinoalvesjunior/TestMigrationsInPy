import pytest
from aiohttp import WebSocketResponse
from aiohttp.test_utils import make_mocked_request

@pytest.fixture
def make_request():
    def maker(method, path, headers=None, protocols=False):
        if headers is None:
            headers = {
                'HOST': 'server.example.com',
                'UPGRADE': 'websocket',
                'CONNECTION': 'Upgrade',
                'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==',
                'ORIGIN': 'http://example.com',
                'SEC-WEBSOCKET-VERSION': '13'
            }
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers)
    return maker

@pytest.mark.asyncio
async def test_close_idempotent(make_request):
    req = make_request('GET', '/')
    ws = WebSocketResponse()
    await ws.prepare(req)
    assert await ws.close(code=1, message='message1')
    assert ws.closed
    assert not await ws.close(code=2, message='message2')