import pytest
from aiohttp import helpers

def test_invalid_formdata_filename():
    form = helpers.FormData()
    invalid_vals = [0, 0.1, {}, [], b'foo']
    for invalid_val in invalid_vals:
        with pytest.raises(TypeError):
            form.add_field('foo', 'bar', filename=invalid_val)