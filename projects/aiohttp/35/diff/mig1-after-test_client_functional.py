import asyncio
import pytest
import aiohttp
from aiohttp import client, test_utils, web

@pytest.mark.run_loop
def test_HTTP_302_REDIRECT_NON_HTTP(create_app_and_client):
    @asyncio.coroutine
    def redirect(request):
        return web.HTTPFound(location='ftp://127.0.0.1/test/')

    app, client = yield from create_app_and_client()
    app.router.add_get('/redirect', redirect)
    with pytest.raises(ValueError):
        yield from client.get('/redirect')