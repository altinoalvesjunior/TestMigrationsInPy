from aiohttp.web import StreamResponse

def test_default_charset():
    resp = StreamResponse()
    assert resp.charset is None