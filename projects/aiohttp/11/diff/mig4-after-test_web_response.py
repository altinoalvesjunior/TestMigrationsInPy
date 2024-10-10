import pytest
from aiohttp.web import Response

def test_ctor_text_body_combined():
    with pytest.raises(ValueError):
        Response(body=b'123', text='test text')