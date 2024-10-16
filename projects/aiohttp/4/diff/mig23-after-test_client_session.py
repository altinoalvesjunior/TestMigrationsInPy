import pytest
import asyncio
from aiohttp.client import ClientSession

@pytest.mark.asyncio
async def test_request_closed_session(loop):
    session = ClientSession(loop=loop)
    session.close()
    with pytest.raises(RuntimeError):
        await session.request('get', '/')