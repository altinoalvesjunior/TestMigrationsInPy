import asyncio
import gc
import unittest
from unittest import mock
import aiohttp
from aiohttp import ClientResponse

class TestBaseConnector(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.transport = unittest.mock.Mock()
        self.stream = aiohttp.StreamParser()
        self.response = ClientResponse('get', 'http://base-conn.org')
        self.response._post_init(self.loop)

    def tearDown(self):
        self.response.close()
        self.loop.close()
        gc.collect()

    def test_del_with_scheduled_cleanup(self):
        conn = aiohttp.BaseConnector(loop=self.loop, keepalive_timeout=0.01)
        transp = unittest.mock.Mock()
        conn._conns['a'] = [(transp, 'proto', 123)]
        conns_impl = conn._conns
        conn._start_cleanup_task()
        exc_handler = unittest.mock.Mock()
        self.loop.set_exception_handler(exc_handler)
        with self.assertWarns(ResourceWarning):
            del conn
            yield from asyncio.sleep(0.01)
            gc.collect()
        self.assertFalse(conns_impl)
        transp.close.assert_called_with()
        msg = {'connector': unittest.mock.ANY,  # conn was deleted
               'message': 'Unclosed connector'}
        if self.loop.get_debug():
            msg['source_traceback'] = unittest.mock.ANY
        exc_handler.assert_called_with(self.loop, msg)