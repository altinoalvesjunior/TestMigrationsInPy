import asyncio
import http.cookies
import io
import json
import pathlib
import socket
import ssl
from unittest import mock

import pytest
from multidict import MultiDict

import aiohttp
from aiohttp import ServerFingerprintMismatch, hdrs, web

async def test_request_conn_closed(test_client):
    async def handler(request):
        request.transport.close()
        return web.Response()
    app = web.Application()
    app.router.add_get('/', handler)
    client = await test_client(app)
    with pytest.raises(aiohttp.ServerDisconnectedError):
        resp = await client.get('/')
        await resp.read()