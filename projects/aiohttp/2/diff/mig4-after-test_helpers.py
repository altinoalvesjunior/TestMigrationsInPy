import pytest
from aiohttp import helpers

def test_invalid_formdata_params2():
    with pytest.raises(TypeError):
        helpers.FormData('as')  # 2-char str is not allowed