from aiohttp.web import StreamResponse
import pytest

def test_charset_without_content_type():
    resp = StreamResponse()

    with pytest.raises(RuntimeError):
        resp.charset = 'koi8-r'