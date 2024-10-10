from aiohttp.web import StreamResponse

def test_drop_content_length_header_on_setting_len_to_None():
    resp = StreamResponse()

    resp.content_length = 1
    assert "1" == resp.headers['Content-Length']
    resp.content_length = None
    assert 'Content-Length' not in resp.headers