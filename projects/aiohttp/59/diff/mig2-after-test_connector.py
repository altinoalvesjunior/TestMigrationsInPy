import asyncio
import os
import ssl
import pytest
import aiohttp
from aiohttp import web

@pytest.mark.asyncio
async def test_tcp_connector_do_not_raise_connector_ssl_error(aiohttp_server):
    async def handler(request):
        return web.Response()

    app = web.Application()
    app.router.add_get('/', handler)

    here = os.path.join(os.path.dirname(__file__), '..', 'tests')
    keyfile = os.path.join(here, 'sample.key')
    certfile = os.path.join(here, 'sample.crt')
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslcontext.load_cert_chain(certfile, keyfile)

    srv = await aiohttp_server(app, ssl=sslcontext)
    port = unused_port()
    conn = aiohttp.TCPConnector(local_addr=('127.0.0.1', port))

    session = aiohttp.ClientSession(connector=conn)
    url = srv.make_url('/')

    r = await session.get(url, ssl=sslcontext)

    r.release()
    first_conn = next(iter(conn._conns.values()))[0][0]

    try:
        _sslcontext = first_conn.transport._ssl_protocol._sslcontext
    except AttributeError:
        _sslcontext = first_conn.transport._sslcontext

    assert _sslcontext is sslcontext
    r.close()

    await session.close()
    conn.close()