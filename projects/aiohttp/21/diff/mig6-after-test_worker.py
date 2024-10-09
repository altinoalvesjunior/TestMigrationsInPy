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


def test_make_handler(worker):
    worker.wsgi = mock.Mock()
    worker.loop = mock.Mock()
    worker.log = mock.Mock()
    worker.cfg = mock.Mock()
    f = worker.make_handler(
        worker.wsgi, 'localhost', 8080)
    assert f is worker.wsgi.make_handler.return_value