import unittest
import asyncio
from aiohttp.client import ClientSession

class TestClientSession(unittest.TestCase):

    def test_request_closed_session(self):
        @asyncio.coroutine
        def go():
            session = ClientSession(loop=self.loop)
            session.close()
            with self.assertRaises(RuntimeError):
                yield from session.request('get', '/')

        self.loop.run_until_complete(go())