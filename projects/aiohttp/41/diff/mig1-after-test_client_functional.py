import asyncio
import io
import json
import pathlib
import ssl
from unittest import mock

import pytest
from multidict import MultiDict

import aiohttp
from aiohttp import hdrs, web
from aiohttp.errors import FingerprintMismatch
from aiohttp.multipart import MultipartWriter

@pytest.mark.run_loop
def test_expect_continue(create_app_and_client):
    expect_called = False
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert data == {'some': 'data'}
        return web.HTTPOk()
    @asyncio.coroutine
    def expect_handler(request):
        nonlocal expect_called
        expect = request.headers.get(hdrs.EXPECT)
        if expect.lower() == "100-continue":
            request.transport.write(b"HTTP/1.1 100 Continue\r\n\r\n")
            expect_called = True
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler, expect_handler=expect_handler)
    resp = yield from client.post('/', data={'some': 'data'}, expect100=True)
    assert 200 == resp.status
    resp.close()
    assert expect_called