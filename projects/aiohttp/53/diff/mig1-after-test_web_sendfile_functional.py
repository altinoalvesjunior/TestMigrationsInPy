import asyncio
import os
import pytest
import aiohttp
from aiohttp import web

try:
    import ssl
except:
    ssl = False

@pytest.mark.skipif(not ssl, reason="ssl not supported")
@asyncio.coroutine
def test_static_file_ssl(loop, test_server, test_client):
    dirname = os.path.dirname(__file__)
    filename = 'data.unknown_mime_type'
    ssl_ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    ssl_ctx.load_cert_chain(
        os.path.join(dirname, 'sample.crt'),
        os.path.join(dirname, 'sample.key')
    )
    app = web.Application(loop=loop)
    app.router.add_static('/static', dirname)
    server = yield from test_server(app, ssl=ssl_ctx)
    conn = aiohttp.TCPConnector(verify_ssl=False, loop=loop)
    client = yield from test_client(server, connector=conn)
    resp = yield from client.get('/static/'+filename)
    assert 200 == resp.status
    txt = yield from resp.text()
    assert 'file content' == txt.rstrip()
    ct = resp.headers['CONTENT-TYPE']
    assert 'application/octet-stream' == ct
    assert resp.headers.get('CONTENT-ENCODING') is None