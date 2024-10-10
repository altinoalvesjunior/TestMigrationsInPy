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
def test_POST_FILES_WITH_DATA(create_app_and_client, fname):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert data['test'] == 'true'
        assert data['some'].content_type in ['application/pgp-keys',
                                             'application/octet-stream']
        assert data['some'].filename == fname.name
        with fname.open('rb') as f:
            assert data['some'].file.read() == f.read()
        return web.HTTPOk()
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    with fname.open() as f:
        resp = yield from client.post('/', data={'test': 'true', 'some': f})
        assert 200 == resp.status
        resp.close()