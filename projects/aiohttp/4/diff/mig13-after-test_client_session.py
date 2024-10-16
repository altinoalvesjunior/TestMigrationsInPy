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

def test_http_POST(session, params):
    with mock.patch("aiohttp.client.ClientSession._request") as patched:
        session.post("http://post.example.com",
                     params={"x": 2},
                     data="Some_data",
                     **params)
    assert patched.called, "`ClientSession._request` not called"
    assert list(patched.call_args) == [("POST", "http://post.example.com",),
                                       dict(
                                           params={"x": 2},
                                           data="Some_data",
                                           **params)]