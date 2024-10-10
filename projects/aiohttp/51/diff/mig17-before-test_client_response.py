import asyncio
import gc
import unittest
from unittest import mock
from yarl import URL
from aiohttp.client_reqrep import ClientResponse

class TestClientResponse(unittest.TestCase:

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

    @mock.patch('aiohttp.client_reqrep.client_logger')
    def test_json_no_content(self, m_log):
        self.response.headers = {
            'Content-Type': 'data/octet-stream'}
        self.response._content = b''
        res = self.loop.run_until_complete(self.response.json())
        self.assertIsNone(res)
        m_log.warning.assert_called_with(
            'Attempt to decode JSON with unexpected mimetype: %s',
            'data/octet-stream')