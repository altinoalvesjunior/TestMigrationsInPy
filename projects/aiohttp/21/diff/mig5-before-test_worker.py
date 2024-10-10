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

    def test_init_signal(self):
        self.worker.loop = unittest.mock.Mock()
        self.worker.init_signal()
        self.assertTrue(self.worker.loop.add_signal_handler.called)