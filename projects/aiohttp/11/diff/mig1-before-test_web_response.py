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

    def test_ctor(self):
        resp = Response()
        self.assertEqual(200, resp.status)
        self.assertEqual('OK', resp.reason)
        self.assertIsNone(resp.body)
        self.assertEqual(0, resp.content_length)
        self.assertEqual(CIMultiDict([('CONTENT-LENGTH', '0')]),
                         resp.headers)