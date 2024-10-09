import functools
import asyncio
import aiohttp.web
from aiohttp.test_utils import make_mocked_request

from aiohttp.web_urldispatcher import (SystemRoute, PlainRoute,
                                       UrlDispatcher)
from aiohttp.web import HTTPCreated, Response

@pytest.mark.run_loop
def test_register_route():
    @asyncio.coroutine
    def handler(request):
        return Response()
    route = PlainRoute('GET', handler, 'test', '/handler/to/path')
    router = UrlDispatcher()
    router.register_route(route)
    req = make_mocked_request('GET', '/handler/to/path')
    info = yield from router.resolve(req)
    assert info is not None
    assert 0 == len(info)
    assert route is info.route
    assert handler is info.handler
    assert info.route.name == 'test'