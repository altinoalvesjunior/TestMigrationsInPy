import asyncio
import pytest
import aiohttp
from aiohttp import web

@asyncio.coroutine
def test_static_file_not_exists(loop, test_client):
    app = web.Application(loop=loop)
    client = yield from test_client(lambda loop: app)
    resp = yield from client.get('/fake')
    assert resp.status == 404
    yield from resp.release()

@asyncio.coroutine
def test_static_file_name_too_long(loop, test_client):
    app = web.Application(loop=loop)
    client = yield from test_client(lambda loop: app)
    resp = yield from client.get('/x*500')
    assert resp.status == 404
    yield from resp.release()

@asyncio.coroutine
def test_static_file_upper_directory(loop, test_client):
    app = web.Application(loop=loop)
    client = yield from test_client(lambda loop: app)
    resp = yield from client.get('/../../')
    assert resp.status == 404
    yield from resp.release()