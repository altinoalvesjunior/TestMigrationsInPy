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
def test_HTTP_200_OK_METHOD_connector(create_app_and_client, loop):
    @asyncio.coroutine
    def handler(request):
        return web.Response(text=request.method)
    conn = aiohttp.TCPConnector(
        conn_timeout=0.2, resolve=True, loop=loop)
    conn.clear_resolved_hosts()
    app, client = yield from create_app_and_client(
        client_params={'connector': conn})
    for meth in ('get', 'post', 'put', 'delete', 'head'):
        app.router.add_route(meth.upper(), '/', handler)
    for meth in ('get', 'post', 'put', 'delete', 'head'):
        resp = yield from client.request(meth, '/')

        content1 = yield from resp.read()
        content2 = yield from resp.read()
        assert content1 == content2
        content = yield from resp.text()

        assert resp.status == 200
        if meth == 'head':
            assert b'' == content1
        else:
            assert meth.upper() == content

        yield from resp.release()