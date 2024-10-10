import asyncio
import unittest
from aiohttp import web

class TestRequestHandlerFactory(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_repr(self):
        app = web.Application(loop=self.loop)
        manager = app.make_handler()
        handler = manager()
        self.assertEqual(
            '<RequestHandler none:none disconnected>', repr(handler))
        handler.transport = object()
        handler._meth = 'GET'
        handler._path = '/index.html'
        self.assertEqual(
            '<RequestHandler GET:/index.html connected>', repr(handler))