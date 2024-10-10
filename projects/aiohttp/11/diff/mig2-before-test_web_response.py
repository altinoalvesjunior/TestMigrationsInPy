import unittest
from unittest import mock
from aiohttp import hdrs, signals
from aiohttp.multidict import CIMultiDict
from aiohttp.web import Response

class TestResponse(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_ctor_with_headers_and_status(self):
        resp = Response(body=b'body', status=201, headers={'Age': '12'})
        self.assertEqual(201, resp.status)
        self.assertEqual(b'body', resp.body)
        self.assertEqual(4, resp.content_length)
        self.assertEqual(CIMultiDict(
            [('AGE', '12'),
             ('CONTENT-LENGTH', '4')]), resp.headers)