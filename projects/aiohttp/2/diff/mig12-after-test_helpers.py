import pytest
from aiohttp import helpers, MultiDict

def test_get_non_existing():
    atoms = helpers.SafeAtoms(
        {}, MultiDict(), MultiDict())
    assert atoms['unknown'] == '-'

def test_get_lower():
    i_headers = MultiDict([('test', '123')])
    o_headers = MultiDict([('TEST', '123')])
    atoms = helpers.SafeAtoms({}, i_headers, o_headers)
    assert atoms['{test}i'] == '123'
    assert atoms['{test}o'] == '-'
    assert atoms['{TEST}o'] == '123'
    assert atoms['{UNKNOWN}o'] == '-'
    assert atoms['{UNKNOWN}'] == '-'