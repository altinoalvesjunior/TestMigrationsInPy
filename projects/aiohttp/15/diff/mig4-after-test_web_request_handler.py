import pytest
from aiohttp import web
from unittest import mock

@pytest.mark.run_loop
def test_finish_connection_timeout(loop):
    app = web.Application(loop=loop)
    manager = app.make_handler()
    handler = mock.Mock()
    transport = mock.Mock()
    manager.connection_made(handler, transport)
    yield from manager.finish_connections(timeout=0.1)
    manager.connection_lost(handler, None)
    assert manager.connections == []
    handler.closing.assert_called_with(timeout=0.09)
    transport.close.assert_called_with()