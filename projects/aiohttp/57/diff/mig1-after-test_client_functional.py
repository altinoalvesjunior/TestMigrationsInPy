
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
from aiohttp.abc import AbstractResolver

async def test_multidict_headers(test_client):
    async def handler(request):
        assert await request.read() == data
        return web.Response()
    app = web.Application()
    app.router.add_post('/', handler)
    client = await test_client(app)
    data = b'sample data'
    r = await client.post('/', data=data,
                          headers=MultiDict(
                              {'Content-Length': str(len(data))}))
    assert r.status == 200