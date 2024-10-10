from aiohttp import web

def test_empty_body_204():
    resp = web.HTTPNoContent()
    assert resp.body is None