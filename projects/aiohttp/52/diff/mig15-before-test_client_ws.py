import asyncio
import unittest
from aiohttp import ClientWebSocketResponse

class TestWebSocketClient(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_receive_runtime_err(self):
        resp = ClientWebSocketResponse(
            mock.Mock(), mock.Mock(), mock.Mock(), mock.Mock(), 10.0,
            True, True, self.loop)
        resp._waiting = True
        self.assertRaises(
            RuntimeError, self.loop.run_until_complete, resp.receive())