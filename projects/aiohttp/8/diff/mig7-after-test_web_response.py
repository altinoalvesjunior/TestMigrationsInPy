from aiohttp.web import StreamResponse

def test_setting_charset():
    resp = StreamResponse()

    resp.content_type = 'text/html'
    resp.charset = 'koi8-r'
    assert 'text/html; charset=koi8-r' == resp.headers['content-type']