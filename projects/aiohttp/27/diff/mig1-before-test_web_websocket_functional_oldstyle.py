import asyncio
import base64
import hashlib
import os
import socket
import unittest

import aiohttp
from aiohttp import helpers, web, websocket


WS_KEY = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"


class TestWebWebSocketFunctional(unittest.TestCase):
    def test_send_recv_text(self):
        closed = helpers.create_future(self.loop)
        @asyncio.coroutine
        def handler(request):
            ws = web.WebSocketResponse()
            yield from ws.prepare(request)
            msg = yield from ws.receive_str()
            ws.send_str(msg+'/answer')
            yield from ws.close()
            closed.set_result(1)
            return ws
        @asyncio.coroutine
        def go():
            _, _, url = yield from self.create_server('GET', '/', handler)
            resp, reader, writer = yield from self.connect_ws(url)
            writer.send('ask')
            msg = yield from reader.read()
            self.assertEqual(msg.tp, websocket.MSG_TEXT)
            self.assertEqual('ask/answer', msg.data)
            msg = yield from reader.read()
            self.assertEqual(msg.tp, websocket.MSG_CLOSE)
            self.assertEqual(msg.data, 1000)
            self.assertEqual(msg.extra, '')
            writer.close()
            yield from closed
            resp.close()
        self.loop.run_until_complete(go())