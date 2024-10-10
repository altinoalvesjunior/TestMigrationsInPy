import asyncio
import gc
import unittest
from unittest import mock
import aiohttp
from aiohttp import helpers, Connection, ClientRequest, ClientResponse

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
    def test_connect(self):
        tr, proto = unittest.mock.Mock(), unittest.mock.Mock()
        proto.is_connected.return_value = True

        req = ClientRequest('GET', 'http://host:80',
                            loop=self.loop,
                            response_class=unittest.mock.Mock())

        conn = aiohttp.BaseConnector(loop=self.loop)
        key = ('host', 80, False)
        conn._conns[key] = [(tr, proto, self.loop.time())]
        conn._create_connection = unittest.mock.Mock()
        conn._create_connection.return_value = helpers.create_future(self.loop)
        conn._create_connection.return_value.set_result((tr, proto))
        connection = yield from conn.connect(req)
        self.assertFalse(conn._create_connection.called)
        self.assertEqual(connection._transport, tr)
        self.assertEqual(connection._protocol, proto)
        self.assertIsInstance(connection, Connection)
        connection.close()