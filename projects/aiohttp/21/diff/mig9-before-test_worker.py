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

    def test_close(self):
        srv = unittest.mock.Mock()
        handler = unittest.mock.Mock()
        self.worker.servers = {srv: handler}
        self.worker.log = unittest.mock.Mock()
        self.worker.loop = self.loop
        app = self.worker.wsgi = unittest.mock.Mock()
        app.finish.return_value = asyncio.Future(loop=self.loop)
        app.finish.return_value.set_result(1)
        handler.connections = [object()]
        handler.finish_connections.return_value = asyncio.Future(
            loop=self.loop)
        handler.finish_connections.return_value.set_result(1)
        self.loop.run_until_complete(self.worker.close())
        app.finish.assert_called_with()
        handler.finish_connections.assert_called_with(timeout=95.0)
        srv.close.assert_called_with()
        self.assertIsNone(self.worker.servers)
        self.loop.run_until_complete(self.worker.close())