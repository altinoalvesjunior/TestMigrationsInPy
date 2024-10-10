import unittest
from unittest import mock
from aiohttp import hdrs, signals
from aiohttp.web import ContentCoding, Request, StreamResponse, Response
from aiohttp.protocol import HttpVersion, HttpVersion11, HttpVersion10
from aiohttp.protocol import RawRequestMessage
from aiohttp.multidict import CIMultiDict

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
    def test_force_compression_gzip(self, ResponseImpl):
        req = self.make_request(
            'GET', '/',
            headers=CIMultiDict({hdrs.ACCEPT_ENCODING: 'gzip, deflate'}))
        resp = StreamResponse()

        resp.enable_compression(ContentCoding.gzip)
        assert resp.compression

        msg = self.loop.run_until_complete(resp.prepare(req))
        msg.add_compression_filter.assert_called_with('gzip')
        assert 'gzip' == resp.headers.get(hdrs.CONTENT_ENCODING)