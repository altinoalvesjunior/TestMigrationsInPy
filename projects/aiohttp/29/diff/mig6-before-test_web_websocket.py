import unittest
from aiohttp import WebSocketResponse

class TestWebWebSocket(unittest.TestCase):

    def test_write(self):
        ws = WebSocketResponse()
        with self.assertRaises(RuntimeError):
            ws.write(b'data')