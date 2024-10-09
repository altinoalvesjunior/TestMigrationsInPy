import pytest
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


def test_init_signal(worker):
    worker.loop = mock.Mock()
    worker.init_signal()
    assert worker.loop.add_signal_handler.called