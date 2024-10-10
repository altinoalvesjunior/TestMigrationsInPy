from aiohttp import web

def test_default_body():
    resp = web.HTTPOk()
    assert b'200: OK' == resp.body