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


def test_run(worker, loop):
    worker.loop = loop
    worker._run = mock.Mock(
        wraps=asyncio.coroutine(lambda: None))
    with pytest.raises(SystemExit):
        worker.run()
    assert worker._run.called
    assert loop._closed