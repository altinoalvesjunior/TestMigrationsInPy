import asyncio
import unittest
import ipaddress
from aiohttp.resolver import AsyncResolver, DefaultResolver

class BaseResolverTestCase(unittest.TestCase):
    __test__ = False

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def test_positive_lookup(self):
        @asyncio.coroutine
        def go():
            real = yield from self.resolver.resolve('www.python.org')
            ipaddress.ip_address(real[0]['host'])
        self.loop.run_until_complete(go())