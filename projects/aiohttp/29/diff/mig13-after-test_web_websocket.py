import pytest
import asyncio
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
async def test_send_str_closed(make_request):
    req = make_request('GET', '/')
    ws = WebSocketResponse()
    await ws.prepare(req)
    await ws.close()
    with pytest.raises(RuntimeError):
        ws.send_str('string')