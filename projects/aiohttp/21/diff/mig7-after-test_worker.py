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


def test__run_ok(worker, loop):
    worker.ppid = 1
    worker.alive = True
    worker.servers = {}
    sock = mock.Mock()
    sock.cfg_addr = ('localhost', 8080)
    worker.sockets = [sock]
    worker.wsgi = mock.Mock()
    worker.close = mock.Mock()
    worker.close.return_value = asyncio.Future(loop=loop)
    worker.close.return_value.set_result(())
    worker.log = mock.Mock()
    worker.notify = mock.Mock()
    worker.loop = loop
    ret = asyncio.Future(loop=loop)
    loop.create_server = mock.Mock(
        wraps=asyncio.coroutine(lambda *a, **kw: ret))
    ret.set_result(sock)
    worker.wsgi.make_handler.return_value.num_connections = 1
    worker.cfg.max_requests = 100
    with mock.patch('aiohttp.worker.asyncio') as m_asyncio:
        m_asyncio.sleep = mock.Mock(
            wraps=asyncio.coroutine(lambda *a, **kw: None))
        loop.run_until_complete(worker._run())
    assert worker.notify.called
    assert worker.log.info.called