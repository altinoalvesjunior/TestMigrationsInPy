import asyncio
import gc
import unittest
import aiohttp
from aiohttp import helpers, ClientRequest, ClientResponse

class TestCookieJarBase(unittest.TestCase):

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

    def test_connect_with_limit_cancelled(self):

        @asyncio.coroutine
        def go():
            tr, proto = unittest.mock.Mock(), unittest.mock.Mock()
            proto.is_connected.return_value = True

            req = ClientRequest('GET', 'http://host:80',
                                loop=self.loop,
                                response_class=unittest.mock.Mock())

            conn = aiohttp.BaseConnector(loop=self.loop, limit=1)
            key = ('host', 80, False)
            conn._conns[key] = [(tr, proto, self.loop.time())]
            conn._create_connection = unittest.mock.Mock()
            conn._create_connection.return_value = helpers.create_future(
                self.loop)
            conn._create_connection.return_value.set_result((tr, proto))

            connection = yield from conn.connect(req)
            self.assertEqual(connection._transport, tr)

            self.assertEqual(1, len(conn._acquired[key]))

            with self.assertRaises(asyncio.TimeoutError):
                # limit exhausted
                yield from asyncio.wait_for(conn.connect(req), 0.01,
                                            loop=self.loop)
            connection.close()
        self.loop.run_until_complete(go())