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

    def test_ctor_text_body_combined(self):
        with self.assertRaises(ValueError):
            Response(body=b'123', text='test text')