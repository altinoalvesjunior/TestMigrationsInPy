import unittest
import unittest.mock
import asyncio
from aiohttp import worker


class MyWorker(worker.GunicornWebWorker):

    def __init__(self):
        self.servers = []
        self.exit_code = 0
        self.cfg = unittest.mock.Mock()
        self.cfg.graceful_timeout = 100


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.worker = MyWorker()

    def tearDown(self):
        self.loop.close()

    def test_run(self):
        self.worker.loop = self.loop
        self.worker._run = unittest.mock.Mock(
            wraps=asyncio.coroutine(lambda: None))
        with self.assertRaises(SystemExit):
            self.worker.run()
        self.assertTrue(self.worker._run.called)
        self.assertTrue(self.loop._closed)