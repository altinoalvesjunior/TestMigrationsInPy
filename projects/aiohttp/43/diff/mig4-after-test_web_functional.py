import asyncio
import json
import pytest
from aiohttp import web

@asyncio.coroutine
def test_post_json(loop, test_client):

    dct = {'key': 'текст'}

    @asyncio.coroutine
    def handler(request):
        data = yield from request.json()
        assert dct == data
        data2 = yield from request.json(loads=json.loads)
        assert data == data2
        with pytest.warns(DeprecationWarning):
            data3 = yield from request.json(loader=json.loads)
        assert data == data3
        resp = web.Response()
        resp.content_type = 'application/json'
        resp.body = json.dumps(data).encode('utf8')
        return resp

    app = web.Application(loop=loop)
    app.router.add_post('/', handler)
    client = yield from test_client(app)

    headers = {'Content-Type': 'application/json'}
    resp = yield from client.post('/', data=json.dumps(dct), headers=headers)
    assert 200 == resp.status
    data = yield from resp.json()
    assert dct == data