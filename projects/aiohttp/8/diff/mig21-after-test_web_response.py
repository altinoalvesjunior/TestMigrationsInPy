import asyncio
import pytest
from unittest import mock
from aiohttp.web import StreamResponse

@pytest.mark.asyncio
async def test_compression_no_accept():
    req = make_request('GET', '/')
    resp = StreamResponse()
    assert not resp.chunked
    assert not resp.compression
    resp.enable_compression()
    assert resp.compression
    with mock.patch('aiohttp.web_reqrep.ResponseImpl') as ResponseImpl:
        msg = await resp.prepare(req)
        assert not msg.add_compression_filter.called