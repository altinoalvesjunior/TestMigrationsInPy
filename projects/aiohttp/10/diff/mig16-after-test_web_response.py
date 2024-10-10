from aiohttp.web import StreamResponse

def test_last_modified_reset():
    resp = StreamResponse()

    resp.last_modified = 0
    resp.last_modified = None
    assert resp.last_modified is None