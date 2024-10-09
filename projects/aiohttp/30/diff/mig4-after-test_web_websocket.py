import pytest
from aiohttp import WebSocketResponse

@pytest.mark.asyncio
async def test_wait_closed_before_start():
    ws = WebSocketResponse()
    with pytest.raises(RuntimeError):
        await ws.close()