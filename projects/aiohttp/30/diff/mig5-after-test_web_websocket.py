import pytest
from aiohttp import WebSocketResponse

@pytest.mark.asyncio
async def test_write_eof_not_started():
    ws = WebSocketResponse()
    with pytest.raises(RuntimeError):
        await ws.write_eof()