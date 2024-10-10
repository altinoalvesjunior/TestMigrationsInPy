import asyncio
import unittest
from aiohttp import WebSocketResponse

class TestWebWebSocket(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def test_write_eof_not_started(self):
        @asyncio.coroutine
        def go():
            ws = WebSocketResponse()
            with self.assertRaises(RuntimeError):
                yield from ws.write_eof()
        self.loop.run_until_complete(go())