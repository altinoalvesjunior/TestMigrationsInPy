from aiohttp.web import StreamResponse

def test_last_modified_initial():
    resp = StreamResponse()
    assert resp.last_modified is None