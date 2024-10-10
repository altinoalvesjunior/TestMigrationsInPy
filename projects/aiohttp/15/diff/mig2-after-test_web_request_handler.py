import pytest
from aiohttp import web

def test_connections(loop):
    app = web.Application(loop=loop)
    manager = app.make_handler()
    assert manager.connections == []
    handler = object()
    transport = object()
    manager.connection_made(handler, transport)
    assert manager.connections == [handler]
    manager.connection_lost(handler, None)
    assert manager.connections == []