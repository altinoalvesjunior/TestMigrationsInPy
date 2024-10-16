import pytest
from unittest import mock
from aiohttp.client import ClientSession

@pytest.fixture
def create_session(loop):
    def maker(*args, **kwargs):
        session = ClientSession(*args, loop=loop, **kwargs)
        return session
    return maker

@pytest.fixture
def session(create_session):
    return create_session()

@pytest.fixture
def params():
    return dict(
        headers={"Authorization": "Basic ..."},
        max_redirects=2,
        encoding="latin1",
        version=aiohttp.HttpVersion10,
        compress="deflate",
        chunked=True,
        expect100=True,
        read_until_eof=False)

def test_http_DELETE(session, params):
    with mock.patch("aiohttp.client.ClientSession._request") as patched:
        session.delete("http://delete.example.com",
                       params={"x": 2},
                       **params)
    assert patched.called, "`ClientSession._request` not called"
    assert list(patched.call_args) == [("DELETE",
                                        "http://delete.example.com",),
                                       dict(
                                           params={"x": 2},
                                           **params)]