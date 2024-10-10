import asyncio
import gc
import unittest
from unittest import mock
from yarl import URL
from aiohttp import helpers
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

    def test_release(self):
        fut = helpers.create_future(self.loop)
        fut.set_result(b'')
        content = self.response.content = mock.Mock()
        content.readany.return_value = fut
        self.loop.run_until_complete(self.response.release())
        self.assertIsNone(self.response._connection)