import asyncio
import pytest
from aiohttp.web import StreamResponse
from aiohttp.protocol import HttpVersion10

@pytest.mark.asyncio
async def test_chunked_encoding_forbidden_for_http_10():
    req = make_request('GET', '/', version=HttpVersion10)
    resp = StreamResponse()
    resp.enable_chunked_encoding()

    with pytest.raises(RuntimeError, match="Using chunked encoding is forbidden for HTTP/1.0"):
        await resp.prepare(req)