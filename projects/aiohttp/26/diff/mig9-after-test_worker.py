import pytest
import asyncio
from unittest import mock
from aiohttp import worker


class MyWorker(worker.GunicornWebWorker):

    def __init__(self):
        self.servers = []
        self.exit_code = 0
        self.cfg = mock.Mock()
        self.cfg.graceful_timeout = 100


@pytest.fixture
def worker():
    return MyWorker()


def test_close(worker, loop):
    srv = mock.Mock()
    handler = mock.Mock()
    worker.servers = {srv: handler}
    worker.log = mock.Mock()
    worker.loop = loop
    app = worker.wsgi = mock.Mock()
    app.finish.return_value = asyncio.Future(loop=loop)
    app.finish.return_value.set_result(1)
    handler.connections = [object()]
    handler.finish_connections.return_value = asyncio.Future(
        loop=loop)
    handler.finish_connections.return_value.set_result(1)
    loop.run_until_complete(worker.close())
    app.finish.assert_called_with()
    handler.finish_connections.assert_called_with(timeout=95.0)
    srv.close.assert_called_with()
    assert worker.servers is None
    loop.run_until_complete(worker.close())