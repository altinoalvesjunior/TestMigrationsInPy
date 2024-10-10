import unittest
import asyncio
from unittest import mock
from aiohttp.web import StreamResponse

class TestStreamResponse(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def make_request(self, method, path, headers=CIMultiDict(),
                     version=HttpVersion11):
        message = RawRequestMessage(method, path, version, headers,
                                    False, False)
        return self.request_from_message(message)

    def request_from_message(self, message):
        self.app = mock.Mock()
        self.app._debug = False
        self.app.on_response_prepare = signals.Signal(self.app)
        self.payload = mock.Mock()
        self.transport = mock.Mock()
        self.reader = mock.Mock()
        self.writer = mock.Mock()
        req = Request(self.app, message, self.payload,
                      self.transport, self.reader, self.writer)
        return req

    @mock.patch('aiohttp.web_reqrep.ResponseImpl')
    def test_chunk_size(self, ResponseImpl):
        req = self.make_request('GET', '/')
        resp = StreamResponse()
        self.assertFalse(resp.chunked)

        resp.enable_chunked_encoding(chunk_size=8192)
        self.assertTrue(resp.chunked)

        msg = self.loop.run_until_complete(resp.prepare(req))
        self.assertTrue(msg.chunked)
        msg.add_chunking_filter.assert_called_with(8192)
        self.assertIsNotNone(msg.filter)