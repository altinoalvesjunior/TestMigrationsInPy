import unittest
from aiohttp import signals
from aiohttp.web import ContentCoding, Request, StreamResponse, Response
from aiohttp.protocol import HttpVersion, HttpVersion10
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

    def test_chunked_encoding_forbidden_for_http_10(self):
        req = self.make_request('GET', '/', version=HttpVersion10)
        resp = StreamResponse()
        resp.enable_chunked_encoding()

        with self.assertRaisesRegex(
                RuntimeError,
                "Using chunked encoding is forbidden for HTTP/1.0"):
            self.loop.run_until_complete(resp.prepare(req))