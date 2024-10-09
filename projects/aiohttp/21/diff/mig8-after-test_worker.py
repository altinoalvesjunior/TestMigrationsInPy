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


def test__run_exc(worker, loop):
    with mock.patch('aiohttp.worker.os') as m_os:
        m_os.getpid.return_value = 1
        m_os.getppid.return_value = 1

        worker.servers = [mock.Mock()]
        worker.ppid = 1
        worker.alive = True
        worker.sockets = []
        worker.log = mock.Mock()
        worker.loop = mock.Mock()
        worker.notify = mock.Mock()
        with mock.patch('aiohttp.worker.asyncio.sleep') as m_sleep:
            slp = asyncio.Future(loop=loop)
            slp.set_exception(KeyboardInterrupt)
            m_sleep.return_value = slp
            worker.close = mock.Mock()
            worker.close.return_value = asyncio.Future(loop=loop)
            worker.close.return_value.set_result(1)
            loop.run_until_complete(worker._run())
        assert m_sleep.called
        assert worker.close.called