import asyncio
import pytest
from unittest import mock
from aiohttp.web import StreamResponse

@pytest.mark.asyncio
async def test_start():
    req = make_request('GET', '/')
    resp = StreamResponse()
    assert resp.keep_alive is None

    with mock.patch('aiohttp.web_reqrep.ResponseImpl') as ResponseImpl:
        msg = await resp.prepare(req)

        assert msg.send_headers.called
        msg2 = await resp.prepare(req)
        assert msg is msg2

        assert resp.keep_alive

    req2 = make_request('GET', '/')
    with pytest.raises(RuntimeError):
        await resp.prepare(req2)