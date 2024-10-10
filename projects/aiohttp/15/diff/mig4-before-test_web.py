import asyncio
import unittest
from unittest import mock
from aiohttp import web

class TestRequestHandlerFactory(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_finish_connection_timeout(self):
        app = web.Application(loop=self.loop)
        manager = app.make_handler()
        handler = mock.Mock()
        transport = mock.Mock()
        manager.connection_made(handler, transport)
        self.loop.run_until_complete(manager.finish_connections(timeout=0.1))
        manager.connection_lost(handler, None)
        self.assertEqual(manager.connections, [])
        handler.closing.assert_called_with(timeout=0.09)
        transport.close.assert_called_with()