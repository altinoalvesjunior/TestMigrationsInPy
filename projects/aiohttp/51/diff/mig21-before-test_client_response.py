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

    @mock.patch('aiohttp.client_reqrep.chardet')
    def test_get_encoding_unknown(self, m_chardet):
        m_chardet.detect.return_value = {'encoding': None}
        self.response.headers = {'Content-Type': 'application/json'}
        self.assertEqual(self.response._get_encoding(), 'utf-8')