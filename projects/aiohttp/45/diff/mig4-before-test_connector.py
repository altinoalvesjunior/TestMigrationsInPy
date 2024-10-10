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

    def test_del_empty_conector(self):
        conn = aiohttp.BaseConnector(loop=self.loop)

        exc_handler = unittest.mock.Mock()
        self.loop.set_exception_handler(exc_handler)

        del conn

        self.assertFalse(exc_handler.called)