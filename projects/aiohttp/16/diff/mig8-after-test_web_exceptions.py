from aiohttp import web

def test_override_body_with_binary():
    txt = "<html><body>Page not found</body></html>"
    resp = web.HTTPNotFound(body=txt.encode('utf-8'),
                            content_type="text/html")
    assert 404 == resp.status
    assert txt.encode('utf-8') == resp.body
    assert txt == resp.text
    assert "text/html" == resp.content_type
    assert resp.charset is None