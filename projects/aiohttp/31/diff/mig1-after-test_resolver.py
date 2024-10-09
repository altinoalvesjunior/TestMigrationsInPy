import pytest
import asyncio
import ipaddress
from aiohttp.resolver import AsyncResolver

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    return loop

def test_async_resolver_positive_lookup(loop):
    @asyncio.coroutine
    def go():
        resolver = AsyncResolver(loop=loop)
        real = yield from resolver.resolve('www.python.org')
        ipaddress.ip_address(real[0]['host'])
    loop.run_until_complete(go())