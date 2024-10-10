import asyncio
import pytest
from aiohttp import ClientWebSocketResponse

@asyncio.coroutine
def test_receive_runtime_err(loop):
    resp = ClientWebSocketResponse(
        mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), 10.0,
        True, True, loop)
    resp._waiting = True
    with pytest.raises(RuntimeError):
        yield from resp.receive()