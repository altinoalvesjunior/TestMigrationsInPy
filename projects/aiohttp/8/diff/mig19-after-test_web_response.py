import asyncio
import pytest
from unittest import mock
from aiohttp.web import StreamResponse

@pytest.mark.asyncio
async def test_chunk_size():
    req = make_request('GET', '/')
    resp = StreamResponse()
    assert not resp.chunked
    resp.enable_chunked_encoding(chunk_size=8192)
    assert resp.chunked
    with mock.patch('aiohttp.web_reqrep.ResponseImpl') as ResponseImpl:
        msg = await resp.prepare(req)
        assert msg.chunked
        msg.add_chunking_filter.assert_called_with(8192)
        assert msg.filter is not None