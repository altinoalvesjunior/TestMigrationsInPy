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

    @unittest.mock.patch('aiohttp.worker.asyncio')
    def test__run(self, m_asyncio):
        self.worker.ppid = 1
        self.worker.alive = True
        self.worker.servers = {}
        sock = unittest.mock.Mock()
        sock.cfg_addr = ('localhost', 8080)
        self.worker.sockets = [sock]
        self.worker.wsgi = unittest.mock.Mock()
        self.worker.close = unittest.mock.Mock()
        self.worker.close.return_value = asyncio.Future(loop=self.loop)
        self.worker.close.return_value.set_result(())
        self.worker.log = unittest.mock.Mock()
        self.worker.notify = unittest.mock.Mock()
        loop = self.worker.loop = unittest.mock.Mock()
        loop.create_server.return_value = asyncio.Future(loop=self.loop)
        loop.create_server.return_value.set_result(sock)
        self.loop.run_until_complete(self.worker._run())
        self.assertTrue(self.worker.log.info.called)
        self.assertTrue(self.worker.notify.called)