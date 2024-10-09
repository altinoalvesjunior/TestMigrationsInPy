import asyncio
import unittest
import socket
from aiohttp.resolver import DefaultResolver

class TestExecutorResolver(unittest.TestCase):
    __test__ = True

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.resolver = DefaultResolver(loop=self.loop)

    def test_negative_lookup(self):
        @asyncio.coroutine
        def go():
            with self.assertRaises(socket.gaierror):
                yield from self.resolver.resolve('doesnotexist.bla')
        self.loop.run_until_complete(go())