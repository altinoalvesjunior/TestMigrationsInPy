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

    def test_make_handler(self):
        self.worker.wsgi = unittest.mock.Mock()
        self.worker.loop = unittest.mock.Mock()
        self.worker.log = unittest.mock.Mock()
        self.worker.cfg = unittest.mock.Mock()
        f = self.worker.make_handler(
            self.worker.wsgi, 'localhost', 8080)
        self.assertIs(f, self.worker.wsgi.make_handler.return_value)