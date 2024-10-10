import asyncio
import gc
import unittest
from unittest import mock
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

class TestClientResponse(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.connection = mock.Mock()
        self.stream = aiohttp.StreamParser(loop=self.loop)
        self.response = ClientResponse('get', URL('http://def-cl-resp.org'))
        self.response._post_init(self.loop)
        self.response._setup_connection(self.connection)

    def tearDown(self):
        self.response.close()
        self.loop.close()
        gc.collect()

    def test_del(self):
        response = ClientResponse('get', URL('http://del-cl-resp.org'))
        response._post_init(self.loop)
        connection = mock.Mock()
        response._setup_connection(connection)
        self.loop.set_exception_handler(lambda loop, ctx: None)
        with self.assertWarns(ResourceWarning):
            del response
            gc.collect()
        connection.close.assert_called_with()