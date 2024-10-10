from aiohttp.web import StreamResponse

def test_ctor():
    resp = StreamResponse()
    assert 200 == resp.status
    assert resp.keep_alive is None