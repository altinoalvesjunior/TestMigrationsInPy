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


def test_init_process(worker):
    with mock.patch('aiohttp.worker.asyncio') as m_asyncio:
        try:
            worker.init_process()
        except TypeError:
            pass

        assert m_asyncio.get_event_loop.return_value.close.called
        assert m_asyncio.new_event_loop.called
        assert m_asyncio.set_event_loop.called