from aiohttp.web import StreamResponse

def test_setting_content_type():
    resp = StreamResponse()

    resp.content_type = 'text/html'
    assert 'text/html' == resp.headers['content-type']