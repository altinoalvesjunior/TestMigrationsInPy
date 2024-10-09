import asyncio
import aiohttp.web

from aiohttp.web_urldispatcher import SystemRoute
from aiohttp.web import HTTPCreated

def test_system_route():
    route = SystemRoute(HTTPCreated(reason='test'))
    assert route.match('any') is None
    with pytest.raises(RuntimeError):
        route.url()
    assert "<SystemRoute 201: test>" == repr(route)
    assert 201 == route.status
    assert 'test' == route.reason