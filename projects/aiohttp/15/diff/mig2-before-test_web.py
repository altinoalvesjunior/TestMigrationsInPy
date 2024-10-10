import asyncio
import unittest
from aiohttp import web

class TestRequestHandlerFactory(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_connections(self):
        app = web.Application(loop=self.loop)
        manager = app.make_handler()
        self.assertEqual(manager.connections, [])
        handler = object()
        transport = object()
        manager.connection_made(handler, transport)
        self.assertEqual(manager.connections, [handler])
        manager.connection_lost(handler, None)
        self.assertEqual(manager.connections, [])