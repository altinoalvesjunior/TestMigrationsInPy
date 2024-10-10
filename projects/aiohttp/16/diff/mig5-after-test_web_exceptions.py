import pytest
from aiohttp import web

def test_HTTPFound_empty_location():
    with pytest.raises(ValueError):
        web.HTTPFound(location='')
    with pytest.raises(ValueError):
        web.HTTPFound(location=None)