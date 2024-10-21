import pytest
from aiohttp import helpers

def test_invalid_formdata_content_transfer_encoding():
    form = helpers.FormData()
    invalid_vals = [0, 0.1, {}, [], b'foo']
    for invalid_val in invalid_vals:
        with pytest.raises(TypeError):
            form.add_field('foo',
                           'bar',
                           content_transfer_encoding=invalid_val)