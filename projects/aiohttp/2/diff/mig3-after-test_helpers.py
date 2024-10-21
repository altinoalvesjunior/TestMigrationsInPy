import pytest
from aiohttp import helpers

def test_invalid_formdata_params():
    with pytest.raises(TypeError):
        helpers.FormData('asdasf')