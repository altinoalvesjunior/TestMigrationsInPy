import pytest
from aiohttp import helpers

def test_basic_auth1():
    # missing password here
    with pytest.raises(ValueError):
        helpers.BasicAuth(None)

def test_basic_auth2():
    with pytest.raises(ValueError):
        helpers.BasicAuth('nkim', None)

def test_basic_auth3():
    auth = helpers.BasicAuth('nkim')
    assert auth.login == 'nkim'
    assert auth.password == ''

def test_basic_auth4():
    auth = helpers.BasicAuth('nkim', 'pwd')
    assert auth.login == 'nkim'
    assert auth.password == 'pwd'
    assert auth.encode() == 'Basic bmtpbTpwd2Q='