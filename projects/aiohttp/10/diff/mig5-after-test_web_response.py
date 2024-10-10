from aiohttp.web import StreamResponse

def test_set_content_length_to_None_on_non_set():
    resp = StreamResponse()

    resp.content_length = None
    assert 'Content-Length' not in resp.headers
    resp.content_length = None
    assert 'Content-Length' not in resp.headers