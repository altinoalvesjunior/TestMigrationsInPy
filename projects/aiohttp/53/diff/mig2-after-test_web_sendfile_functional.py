import asyncio
import os
import pytest
import aiohttp
from aiohttp import web

@asyncio.coroutine
def test_static_file_directory_traversal_attack(loop, test_client):
    dirname = os.path.dirname(__file__)
    relpath = '../README.rst'
    assert os.path.isfile(os.path.join(dirname, relpath))

    app = web.Application(loop=loop)
    app.router.add_static('/static', dirname)
    client = yield from test_client(app)
    resp = yield from client.get('/static/'+relpath)
    assert 404 == resp.status
    url_relpath2 = '/static/dir/../' + relpath
    resp = yield from client.get(url_relpath2)
    assert 404 == resp.status
    url_abspath = \
        '/static/' + os.path.abspath(os.path.join(dirname, relpath))
    resp = yield from client.get(url_abspath)
    assert 404 == resp.status