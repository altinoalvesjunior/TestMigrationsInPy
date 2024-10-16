import pytest
import asyncio
from unittest import mock
from aiohttp.client import ClientSession

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

@pytest.mark.asyncio
async def test_reraise_os_error(create_session):
    err = OSError(1, "permission error")
    req = mock.Mock()
    req_factory = mock.Mock(return_value=req)
    req.send = mock.Mock(side_effect=err)
    session = create_session(request_class=req_factory)
    async def create_connection(req):
        # return self.transport, self.protocol
        return mock.Mock(), mock.Mock()
    session._connector._create_connection = create_connection
    with pytest.raises(aiohttp.ClientOSError) as ctx:
        await session.request('get', 'http://example.com')
    e = ctx.value
    assert e.errno == err.errno
    assert e.strerror == err.strerror