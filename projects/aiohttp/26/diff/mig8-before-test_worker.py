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

    @unittest.mock.patch('aiohttp.worker.os')
    @unittest.mock.patch('aiohttp.worker.asyncio.sleep')
    def test__run_exc(self, m_sleep, m_os):
        m_os.getpid.return_value = 1
        m_os.getppid.return_value = 1

        self.worker.servers = [unittest.mock.Mock()]
        self.worker.ppid = 1
        self.worker.alive = True
        self.worker.sockets = []
        self.worker.log = unittest.mock.Mock()
        self.worker.loop = unittest.mock.Mock()
        self.worker.notify = unittest.mock.Mock()
        slp = asyncio.Future(loop=self.loop)
        slp.set_exception(KeyboardInterrupt)
        m_sleep.return_value = slp
        self.worker.close = unittest.mock.Mock()
        self.worker.close.return_value = asyncio.Future(loop=self.loop)
        self.worker.close.return_value.set_result(1)
        self.loop.run_until_complete(self.worker._run())
        self.assertTrue(m_sleep.called)
        self.assertTrue(self.worker.close.called)