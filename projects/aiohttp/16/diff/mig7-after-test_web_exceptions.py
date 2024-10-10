from aiohttp import web

def test_override_body_with_text():
    resp = web.HTTPNotFound(text="Page not found")
    assert 404 == resp.status
    assert "Page not found".encode('utf-8') == resp.body
    assert "Page not found" == resp.text
    assert "text/plain" == resp.content_type
    assert "utf-8" == resp.charset