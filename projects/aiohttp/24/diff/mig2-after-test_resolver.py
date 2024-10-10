import pytest
import asyncio
import ipaddress
from aiohttp.resolver import AsyncResolver

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    return loop

def test_async_resolver_multiple_replies(loop):
    @asyncio.coroutine
    def go():
        resolver = AsyncResolver(loop=loop)
        real = yield from resolver.resolve('www.google.com')
        ips = [ipaddress.ip_address(x['host']) for x in real]
        assert len(ips) > 3, "Expecting multiple addresses"
    loop.run_until_complete(go())