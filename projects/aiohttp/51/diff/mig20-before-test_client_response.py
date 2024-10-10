import asyncio
import gc
import unittest
from unittest import mock
from yarl import URL
from aiohttp import helpers, StreamReader
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

    def test_override_flow_control(self):
        class MyResponse(ClientResponse):
            flow_control_class = StreamReader
        response = MyResponse('get', URL('http://my-cl-resp.org'))
        response._post_init(self.loop)
        response._setup_connection(self.connection)
        self.assertIsInstance(response.content, StreamReader)
        response.close()