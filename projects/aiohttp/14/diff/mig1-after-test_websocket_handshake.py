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

def test_not_get(message, transport):
    with pytest.raises(errors.HttpProcessingError):
        websocket.do_handshake('POST', message.headers, transport)