import unittest
from aiohttp import WebSocketResponse

class TestWebWebSocket(unittest.TestCase):

    def test_closed_after_ctor(self):
        ws = WebSocketResponse()
        self.assertFalse(ws.closed)
        self.assertIsNone(ws.close_code)