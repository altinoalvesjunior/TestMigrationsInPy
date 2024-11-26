import base64
import hashlib
import os
import pytest
from aiohttp import websocket, multidict, protocol, errors
from unittest import mock

@pytest.fixture()
def transport():
    return mock.Mock()

@pytest.fixture()
def message():
    headers = multidict.MultiDict()
    return protocol.RawRequestMessage(
        'GET', '/path', (1, 0), headers, True, None)

def test_handshake_protocol(message, transport):
    proto = 'chat'
    message.headers.extend(gen_ws_headers(proto)[0])
    _, resp_headers, _, _, protocol = websocket.do_handshake(
        message.method, message.headers, transport,
        protocols=[proto])
    assert protocol == proto