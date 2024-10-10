import asyncio
import gc
import unittest
from unittest import mock
import aiohttp
from aiohttp import helpers, ClientRequest, ClientResponse

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

    @asyncio.coroutine
    def test_connect_oserr(self):
        conn = aiohttp.BaseConnector(loop=self.loop)
        conn._create_connection = unittest.mock.Mock()
        conn._create_connection.return_value = helpers.create_future(self.loop)
        err = OSError(1, 'permission error')
        conn._create_connection.return_value.set_exception(err)
        with self.assertRaises(aiohttp.ClientOSError) as ctx:
            req = unittest.mock.Mock()
            yield from conn.connect(req)
        self.assertEqual(1, ctx.exception.errno)
        self.assertTrue(ctx.exception.strerror.startswith('Cannot connect to'))
        self.assertTrue(ctx.exception.strerror.endswith('[permission error]'))