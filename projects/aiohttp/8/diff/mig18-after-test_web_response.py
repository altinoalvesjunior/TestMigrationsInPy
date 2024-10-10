import asyncio
import pytest
from unittest import mock
from aiohttp.web import StreamResponse

@pytest.mark.asyncio
async def test_chunked_encoding():
    req = make_request('GET', '/')
    resp = StreamResponse()
    assert not resp.chunked
    resp.enable_chunked_encoding()
    assert resp.chunked
    with mock.patch('aiohttp.web_reqrep.ResponseImpl') as ResponseImpl:
        msg = await resp.prepare(req)
        assert msg.chunked