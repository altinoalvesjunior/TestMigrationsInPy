from aiohttp import web

def test_empty_body_205():
    resp = web.HTTPNoContent()
    assert resp.body is None