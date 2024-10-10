import asyncio
import io
import os
import os.path
import ssl
from unittest import mock

import pytest

import aiohttp
from aiohttp import hdrs, web
from aiohttp.errors import FingerprintMismatch

@pytest.mark.run_loop
def test_HTTP_302_REDIRECT_GET(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        return web.Response(text=request.method)
    @asyncio.coroutine
    def redirect(request):
        return web.HTTPFound(location='/')
    app, client = yield from create_app_and_client()
    app.router.add_get('/', handler)
    app.router.add_get('/redirect', redirect)
    resp = yield from client.get('/redirect')
    assert 200 == resp.status
    assert 1 == len(resp.history)
    resp.close()