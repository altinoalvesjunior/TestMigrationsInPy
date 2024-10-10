from aiohttp.web import StreamResponse

def test_content_length():
    resp = StreamResponse()
    assert resp.content_length is None