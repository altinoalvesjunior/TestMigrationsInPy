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
def test_POST_FILES_IO_WITH_PARAMS(create_app_and_client):
    @asyncio.coroutine
    def handler(request):
        data = yield from request.post()
        assert data['test'] == 'true'
        assert data['unknown'].content_type == 'application/octet-stream'
        assert data['unknown'].filename == 'unknown'
        assert data['unknown'].file.read() == b'data'
        assert data.getall('q') == ['t1', 't2']
        return web.HTTPOk()
    
    app, client = yield from create_app_and_client()
    app.router.add_post('/', handler)
    data = io.BytesIO(b'data')
    resp = yield from client.post('/', data=(('test', 'true'),
                                             MultiDict([('q', 't1'), ('q', 't2')]),
                                             data))
    assert 200 == resp.status
    resp.close()