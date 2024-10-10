import unittest
import unittest.mock
from aiohttp import worker


class MyWorker(worker.GunicornWebWorker):

    def __init__(self):
        self.servers = []
        self.exit_code = 0
        self.cfg = unittest.mock.Mock()
        self.cfg.graceful_timeout = 100


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.worker = MyWorker()

    @unittest.mock.patch('aiohttp.worker.asyncio')
    def test_init_process(self, m_asyncio):
        try:
            self.worker.init_process()
        except TypeError:
            pass

        self.assertTrue(m_asyncio.get_event_loop.return_value.close.called)
        self.assertTrue(m_asyncio.new_event_loop.called)
        self.assertTrue(m_asyncio.set_event_loop.called)