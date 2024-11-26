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

def test_handshake(message, transport):
    hdrs, sec_key = gen_ws_headers()
    message.headers.extend(hdrs)
    status, headers, parser, writer, protocol = websocket.do_handshake(
        message.method, message.headers, transport)
    assert status == 101
    assert protocol is None