import pytest
from aiohttp import helpers

def test_get_seconds_and_milliseconds():
    response = dict(status=200, output_length=1)
    request_time = 321.012345678901234
    atoms = helpers.atoms(None, None, response, None, request_time)
    assert atoms['T'] == '321'
    assert atoms['D'] == '012345'