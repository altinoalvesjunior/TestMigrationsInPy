import unittest
from unittest import mock
from aiohttp import hdrs, signals
from aiohttp.web import Request, StreamResponse, Response
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

    def test_cannot_write_eof_twice(self):
        resp = StreamResponse()
        writer = mock.Mock()
        self.loop.run_until_complete(
            resp.prepare(self.make_request('GET', '/', writer=writer)))

        resp.write(b'data')
        writer.drain.return_value = ()
        self.loop.run_until_complete(resp.write_eof())
        assert writer.write.called

        writer.write.reset_mock()
        self.loop.run_until_complete(resp.write_eof())
        assert not writer.write.called