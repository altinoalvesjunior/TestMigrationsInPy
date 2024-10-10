import asyncio
import unittest
from unittest import mock
from aiohttp.multidict import CIMultiDict
from aiohttp.web import Request
from aiohttp import signals, web

class TestHTTPExceptions(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.payload = mock.Mock()
        self.transport = mock.Mock()
        self.reader = mock.Mock()
        self.writer = mock.Mock()
        self.writer.drain.return_value = ()
        self.buf = b''
        self.writer.write.side_effect = self.append

    def tearDown(self):
        self.loop.close()

    def append(self, data):
        self.buf += data

    def make_request(self, method='GET', path='/', headers=CIMultiDict()):
        self.app = mock.Mock()
        self.app._debug = False
        self.app.on_response_prepare = signals.Signal(self.app)
        message = RawRequestMessage(method, path, HttpVersion11, headers,
                                    False, False)
        req = Request(self.app, message, self.payload,
                      self.transport, self.reader, self.writer)
        return req

    def test_HTTPFound(self):
        req = self.make_request()
        resp = web.HTTPFound(location='/redirect')
        self.assertEqual('/redirect', resp.location)
        self.assertEqual('/redirect', resp.headers['location'])
        self.loop.run_until_complete(resp.prepare(req))
        self.loop.run_until_complete(resp.write_eof())
        txt = self.buf.decode('utf8')
        self.assertRegex(txt, ('HTTP/1.1 302 Found\r\n'
                               'CONTENT-TYPE: text/plain; charset=utf-8\r\n'
                               'CONTENT-LENGTH: 10\r\n'
                               'LOCATION: /redirect\r\n'
                               'CONNECTION: keep-alive\r\n'
                               'DATE: .+\r\n'
                               'SERVER: .+\r\n\r\n'
                               '302: Found'))