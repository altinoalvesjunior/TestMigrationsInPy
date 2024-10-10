import asyncio
import unittest
import aiodns
from aiohttp.resolver import AsyncResolver

class TestAsyncResolver(unittest.TestCase):
    __test__ = True

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.resolver = AsyncResolver(loop=self.loop)

    def test_negative_lookup(self):
        @asyncio.coroutine
        def go():
            with self.assertRaises(aiodns.error.DNSError):
                yield from self.resolver.resolve('doesnotexist.bla')
        self.loop.run_until_complete(go())