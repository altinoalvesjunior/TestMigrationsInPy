import asyncio
import unittest
from aiohttp import WebSocketResponse

class TestWebWebSocket(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def test_wait_closed_before_start(self):
        @asyncio.coroutine
        def go():
            ws = WebSocketResponse()
            with self.assertRaises(RuntimeError):
                yield from ws.close()
        self.loop.run_until_complete(go())