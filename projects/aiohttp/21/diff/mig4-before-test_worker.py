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

    def test_handle_abort(self):
        self.worker.handle_abort(object(), object())
        self.assertEqual(self.worker.alive, False)
        self.assertEqual(self.worker.exit_code, 1)