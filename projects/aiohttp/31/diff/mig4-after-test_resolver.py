import pytest
import asyncio
import socket
from aiohttp.resolver import DefaultResolver

@pytest.fixture
def loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(None)
    return loop

def test_default_negative_lookup(loop):
    @asyncio.coroutine
    def go():
        resolver = DefaultResolver(loop=loop)
        try:
            yield from resolver.resolve('doesnotexist.bla')
            assert False, "Expecting socket.gaierror"
        except socket.gaierror:
            pass
    loop.run_until_complete(go())