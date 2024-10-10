import asyncio
import pathlib
import pytest
import aiohttp
from aiohttp import web

@pytest.fixture
def sender():
    def maker(*args, **kwargs):
        return aiohttp.FileSender(*args, **kwargs)
    return maker

@pytest.fixture
def filepath():
    return pathlib.Path(__file__).parent / 'data.unknown_mime_type'

@asyncio.coroutine
def test_static_file_ok(loop, test_client, sender, filepath):
    @asyncio.coroutine
    def handler(request):
        resp = yield from sender().send(request, filepath)
        return resp
    app = web.Application(loop=loop)
    app.router.add_get('/', handler)
    client = yield from test_client(lambda loop: app)
    resp = yield from client.get('/')
    assert resp.status == 200
    txt = yield from resp.text()
    assert 'file content' == txt.rstrip()
    assert 'application/octet-stream' == resp.headers['Content-Type']
    assert resp.headers.get('Content-Encoding') is None
    yield from resp.release()