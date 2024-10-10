import pytest
from aiohttp import WebSocketResponse, CIMultiDict
from aiohttp.test_utils import make_mocked_request

@pytest.fixture
def make_request():
    def maker(method, path, headers=None, protocols=False):
        if headers is None:
            headers = CIMultiDict({
                'HOST': 'server.example.com',
                'UPGRADE': 'websocket',
                'CONNECTION': 'Upgrade',
                'SEC-WEBSOCKET-KEY': 'dGhlIHNhbXBsZSBub25jZQ==',
                'ORIGIN': 'http://example.com',
                'SEC-WEBSOCKET-VERSION': '13'
            })
        if protocols:
            headers['SEC-WEBSOCKET-PROTOCOL'] = 'chat, superchat'
        return make_mocked_request(method, path, headers)
    return maker

def test_can_prepare_without_upgrade(make_request):
    req = make_request('GET', '/', headers=CIMultiDict({}))
    ws = WebSocketResponse()
    assert (False, None) == ws.can_prepare(req)