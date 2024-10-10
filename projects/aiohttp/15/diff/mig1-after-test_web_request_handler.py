import pytest
from aiohttp import web

def test_repr(loop):
    app = web.Application(loop=loop)
    manager = app.make_handler()
    handler = manager()
    assert '<RequestHandler none:none disconnected>' == repr(handler)
    handler.transport = object()
    handler._meth = 'GET'
    handler._path = '/index.html'
    assert '<RequestHandler GET:/index.html connected>' == repr(handler)