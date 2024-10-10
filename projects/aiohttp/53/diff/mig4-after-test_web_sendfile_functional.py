import asyncio
import os
import pytest
from aiohttp import web

@asyncio.coroutine
def test_static_file_huge(loop, test_client, tmpdir):
    filename = 'huge_data.unknown_mime_type'
    # fill 100MB file
    with tmpdir.join(filename).open('w') as f:
        for i in range(1024*20):
            f.write(chr(i % 64 + 0x20) * 1024)
    file_st = os.stat(str(tmpdir.join(filename)))
    app = web.Application(loop=loop)
    app.router.add_static('/static', str(tmpdir))
    client = yield from test_client(app)
    resp = yield from client.get('/static/'+filename)
    assert 200 == resp.status
    ct = resp.headers['CONTENT-TYPE']
    assert 'application/octet-stream' == ct
    assert resp.headers.get('CONTENT-ENCODING') is None
    assert int(resp.headers.get('CONTENT-LENGTH')) == file_st.st_size
    f = tmpdir.join(filename).open('rb')
    off = 0
    cnt = 0
    while off < file_st.st_size:
        chunk = yield from resp.content.readany()
        expected = f.read(len(chunk))
        assert chunk == expected
        off += len(chunk)
        cnt += 1
    f.close()