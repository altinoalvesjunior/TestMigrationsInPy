import unittest
from aiohttp.web import StreamResponse

def test_charset_without_content_type(self):
    resp = StreamResponse()

    with pytest.raises(RuntimeError):
        resp.charset = 'koi8-r'