import asyncio
import unittest
import ipaddress
from aiohttp.resolver import AsyncResolver, DefaultResolver

class BaseResolverTestCase(unittest.TestCase):
    __test__ = False

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def test_multiple_replies(self):
        @asyncio.coroutine
        def go():
            real = yield from self.resolver.resolve('www.google.com')
            ips = [ipaddress.ip_address(x['host']) for x in real]
            self.assertGreater(len(ips), 3)
        self.loop.run_until_complete(go())