import pytest
import asyncio
import aiodns
from aiohttp.resolver import AsyncResolver

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    return loop

def test_async_negative_lookup(loop):
    @asyncio.coroutine
    def go():
        resolver = AsyncResolver(loop=loop)
        try:
            yield from resolver.resolve('doesnotexist.bla')
            assert False, "Expecting aiodns.error.DNSError"
        except aiodns.error.DNSError:
            pass
    loop.run_until_complete(go())